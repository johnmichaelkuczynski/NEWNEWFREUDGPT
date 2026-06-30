import { chat } from "./openai";
import { searchPositions, formatPositionsForContext, deduce } from "./inference";
import { LongFormState, SkeletonSection, Skeleton, StateUpdate } from "./coherenceState";

const THINKERS_WITH_INFERENCE = ["kuczynski", "nietzsche", "bergler"];

function extractJson(raw: string): string | null {
  const cleaned = raw
    .trim()
    .replace(/```json\s*/gi, "")
    .replace(/```\s*/g, "")
    .replace(/,(\s*[}\]])/g, "$1");
  let depth = 0;
  let start = -1;
  for (let i = 0; i < cleaned.length; i++) {
    if (cleaned[i] === "{") {
      if (start === -1) start = i;
      depth++;
    } else if (cleaned[i] === "}") {
      depth--;
      if (depth === 0 && start !== -1) return cleaned.slice(start, i + 1);
    }
  }
  return null;
}

/**
 * Pack the full anti-repetition list within a character budget.
 * For 50K-word jobs this can grow to hundreds of items; we keep the most-recent
 * fully and elide the middle if needed, so both the start AND the end of the
 * argument remain protected against repetition.
 */
function packAntiRepeat(items: string[], charBudget: number): string {
  if (!items.length) return "";
  const lines = items.map((c) => `× ${c}`);
  const joined = lines.join("\n");
  if (joined.length <= charBudget) return joined;
  // Keep first 30% and last 70%, with an elision marker
  const headChars = Math.floor(charBudget * 0.3);
  const tailChars = charBudget - headChars - 40;
  let head: string[] = [];
  let headLen = 0;
  for (const l of lines) {
    if (headLen + l.length + 1 > headChars) break;
    head.push(l);
    headLen += l.length + 1;
  }
  let t: string[] = [];
  let tailLen = 0;
  for (let i = lines.length - 1; i >= 0; i--) {
    if (tailLen + lines[i].length + 1 > tailChars) break;
    t.unshift(lines[i]);
    tailLen += lines[i].length + 1;
  }
  return [...head, `× [... ${lines.length - head.length - t.length} earlier items elided ...]`, ...t].join("\n");
}

function summariesContext(state: LongFormState, currentIdx: number, charBudget = 6000): string {
  const items = (state.section_summaries || []).filter((s) => s.i < currentIdx);
  if (!items.length) return "(none yet — this is the opening section)";
  const lines = items.map((s) => `[§${s.i + 1} ${s.title}] ${s.summary}`);
  // Trim from the front if budget exceeded — keep the most recent summaries fully
  while (lines.join("\n").length > charBudget && lines.length > 8) {
    lines.shift();
  }
  return lines.join("\n");
}

export async function generateCoherentSection(
  thinker: string,
  skeleton: Skeleton,
  state: LongFormState,
  sectionPlan: SkeletonSection,
  mode: string
): Promise<string> {
  const thinkerLower = thinker.toLowerCase();

  // Retrieve positions per micro-plan query (limit to keep prompt size manageable)
  const positionResults: any[] = [];
  const seenIds = new Set<string>(state.positions_cited);
  for (const query of (sectionPlan.positions_to_use || []).slice(0, 4)) {
    try {
      const results = await searchPositions(thinkerLower, query, 5);
      for (const p of results) {
        if (!seenIds.has(p.id)) {
          seenIds.add(p.id);
          positionResults.push(p);
        }
        if (positionResults.length >= 12) break;
      }
      if (positionResults.length >= 12) break;
    } catch {}
  }
  const positionsContext = positionResults.length
    ? formatPositionsForContext(positionResults)
    : "";

  // Optional inference chain for thinkers with engines
  let inferenceChain = "";
  if (THINKERS_WITH_INFERENCE.includes(thinkerLower)) {
    try {
      const ctx = `${sectionPlan.title} ${sectionPlan.claims_to_make.join("; ")}`;
      inferenceChain = await deduce(thinkerLower, ctx, 8);
    } catch {}
  }

  // Use the FULL claims/examples list (with mid-elision if the budget overflows)
  // so late sections of a 50K-word document still see early claims and don't repeat them.
  const claimsBlock = packAntiRepeat(state.claims_made, 5000);
  const examplesBlock = packAntiRepeat(state.examples_used, 2000);
  const summaries = summariesContext(state, sectionPlan.index, 6000);
  const openThreads = (state.open_threads || []).slice(0, 12);
  const isFinal = sectionPlan.index === skeleton.sections.length - 1;
  const isOpening = sectionPlan.index === 0;

  const modeNote =
    mode === "dialogue"
      ? `This is one TURN/BEAT in a continuous dialogue. Use named speakers consistently with prior sections. Do not restart the dialogue or re-introduce speakers. Carry the conversation forward.`
      : mode === "lecture"
      ? `This is one teaching unit in an ongoing lecture. Do not re-introduce the subject or restate the lecture's purpose. Continue from where the previous unit left off.`
      : `This is ONE section of a continuous long-form essay. Do NOT write a self-contained mini-essay. Do not re-introduce the thesis. Do not summarize prior sections. Continue the argument forward.`;

  const system = `You are ${thinker}. Write exclusively in ${thinker}'s authentic voice, vocabulary, rhetorical patterns, and characteristic moves. Never break character. Never use meta-commentary like "in this section" or "now I will discuss". Never use markdown headings, bold, or bullet points — write flowing prose only.`;

  const positionsSection = positionsContext
    ? `\n\nRELEVANT POSITIONS FROM YOUR CORPUS (use them — quote or closely paraphrase, do not invent):\n${positionsContext}`
    : "";
  const inferenceSection = inferenceChain
    ? `\n\nINFERENCE CHAIN (apply these principles):\n${inferenceChain}`
    : "";

  const bridgeBlock = isOpening
    ? `OPENING — establish the question, scene, or provocation. Do NOT preamble with "I will argue" or list what's to come.`
    : `BRIDGE: ${sectionPlan.bridge_from_prior || "(carry forward from prior section)"}\n\nLAST PARAGRAPH OF PRIOR SECTION (continue seamlessly from this — your first sentence must follow naturally from its last sentence):\n"${state.last_paragraph || "(none)"}"`;

  const prompt = `OVERALL THESIS: ${skeleton.thesis}
NARRATIVE ARC: ${skeleton.arc}
CENTRAL CONCEPTS (recur throughout): ${(skeleton.central_concepts || []).join(", ")}

CURRENT POSITION IN ARC: Section ${sectionPlan.index + 1} of ${skeleton.sections.length} — role: ${sectionPlan.role}
SECTION TITLE: ${sectionPlan.title}

${modeNote}

${bridgeBlock}

WHAT THIS SECTION MUST ACCOMPLISH (every claim below must appear, integrated into your prose — not as a list):
${sectionPlan.claims_to_make.map((c, i) => `${i + 1}. ${c}`).join("\n")}

EXAMPLES TO DEPLOY HERE (use them concretely, not as passing mentions):
${(sectionPlan.examples_to_use || []).map((e) => `- ${e}`).join("\n") || "(no required examples)"}

OPEN THREADS YOU MAY DISCHARGE (mark which one(s) you resolve in your section_summary later):
${openThreads.length ? openThreads.map((t) => `- ${t}`).join("\n") : "(none)"}

ANTI-REPETITION RULES — CLAIMS ALREADY ESTABLISHED EARLIER. DO NOT RESTATE OR ARGUE FOR THEM AGAIN (you may *refer back* to them, but never re-derive):
${(sectionPlan.must_not_repeat || []).map((c) => `× ${c}`).join("\n")}
${claimsBlock || "(no prior claims yet)"}

EXAMPLES / CASES ALREADY DEPLOYED IN PRIOR SECTIONS — DO NOT REUSE THE SAME EXAMPLES (find new ones):
${examplesBlock || "(none yet)"}

PRIOR SECTION SUMMARIES (for context — do NOT recap them in your prose):
${summaries}
${positionsSection}${inferenceSection}

WHAT MUST BE SET UP FOR THE NEXT SECTION:
${isFinal ? "(none — this is the final section, close the arc decisively without 'in conclusion' phrasing)" : sectionPlan.bridge_to_next || "Leave the next section something to develop."}

LENGTH TARGET: approximately ${sectionPlan.word_target} words. Do not pad. Do not truncate. Write tight, dense prose.

Now write the section. Pure prose only. Begin directly — no heading, no title, no "Section N:". Your first sentence must continue from the prior section's last paragraph (unless this is the opening). Do not announce what you are about to do; do it.`;

  const maxTokens = Math.min(8000, Math.round(sectionPlan.word_target * 1.6) + 600);
  const text = await chat(system, prompt, { maxTokens });
  return text.trim();
}

export async function extractStateUpdate(
  thinker: string,
  sectionPlan: SkeletonSection,
  sectionText: string,
  priorState: LongFormState,
  skeleton: Skeleton
): Promise<StateUpdate> {
  const isFinal = sectionPlan.index === skeleton.sections.length - 1;
  const system = `You are a coherence-state extractor. Output ONLY valid JSON. No commentary, no markdown fences.`;

  // Trim section text if very long for the extraction call
  const trimmedText =
    sectionText.length > 12000
      ? sectionText.slice(0, 6000) + "\n\n[... middle elided ...]\n\n" + sectionText.slice(-6000)
      : sectionText;

  const prompt = `A new section was just written. Extract the state delta.

OVERALL THESIS: ${skeleton.thesis}

SECTION ${sectionPlan.index + 1} of ${skeleton.sections.length} — "${sectionPlan.title}" (role: ${sectionPlan.role})

PLANNED CLAIMS FOR THIS SECTION:
${sectionPlan.claims_to_make.map((c) => `- ${c}`).join("\n")}

PRIOR OPEN THREADS:
${(priorState.open_threads || []).map((t) => `- ${t}`).join("\n") || "(none)"}

SECTION TEXT JUST WRITTEN:
"""
${trimmedText}
"""

Output ONLY this JSON:
{
  "new_claims": ["List the distinct claims this section actually established — short propositional phrases, 5-15 items. Use claims_to_make as a guide but extract from the actual text."],
  "new_positions_cited": ["List any quoted or paraphrased source positions referenced — use short identifying labels like author + concept"],
  "new_examples": ["List concrete examples, cases, or thought experiments deployed in this section — short noun phrases"],
  "new_open_threads": ["Promises, anticipations, or unanswered questions the section LEAVES OPEN for later sections to address. ${isFinal ? "Should be empty for final section." : ""}"],
  "resolved": ["From the prior open threads above, list any that this section discharged. Use the exact wording of the prior open thread."],
  "section_summary": "1-2 sentences: what this section established and where it left the argument.",
  "last_paragraph": "Copy verbatim the LAST PARAGRAPH (final 80-200 words) of the section text above, so the next section can bridge from it.",
  "next_stage": "${isFinal ? "conclusion" : "intro|development|objection|reply|synthesis|conclusion"}"
}`;

  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const raw = await chat(system, prompt, { maxTokens: 2500 });
      const j = extractJson(raw);
      if (!j) continue;
      const parsed = JSON.parse(j) as StateUpdate;
      // Ensure last_paragraph populated even if LLM forgets
      if (!parsed.last_paragraph) {
        const paragraphs = sectionText.split(/\n\s*\n/).filter((p) => p.trim().length > 0);
        parsed.last_paragraph = paragraphs[paragraphs.length - 1] || sectionText.slice(-500);
      }
      return parsed;
    } catch (e) {
      console.error(`State extract attempt ${attempt + 1} failed:`, e);
    }
  }

  // Fallback: salvage what we can without an LLM
  const paragraphs = sectionText.split(/\n\s*\n/).filter((p) => p.trim().length > 0);
  return {
    new_claims: sectionPlan.claims_to_make,
    new_positions_cited: [],
    new_examples: sectionPlan.examples_to_use || [],
    new_open_threads: [],
    resolved: [],
    section_summary: `Section ${sectionPlan.index + 1} addressed: ${sectionPlan.title}.`,
    last_paragraph: paragraphs[paragraphs.length - 1] || sectionText.slice(-500),
    next_stage: isFinal ? "conclusion" : undefined,
  };
}
