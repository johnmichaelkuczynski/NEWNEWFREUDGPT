import { chat } from "./openai";
import { Skeleton, SkeletonSection } from "./coherenceState";
import { searchPositions } from "./inference";

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
      if (depth === 0 && start !== -1) {
        return cleaned.slice(start, i + 1);
      }
    }
  }
  return null;
}

interface MacroPlan {
  thesis: string;
  central_concepts: string[];
  arc: string;
  macro_sections: { title: string; role: string; gist: string; word_target: number }[];
}

async function generateMacroPlan(
  thinker: string,
  userPrompt: string,
  mode: string,
  targetWords: number
): Promise<MacroPlan> {
  // Calibrate section count: aim ~2000-2500 words per section, min 5, max 30
  const wordsPerSection = 2200;
  const sectionCount = Math.max(5, Math.min(30, Math.round(targetWords / wordsPerSection)));

  const modeNote =
    mode === "dialogue"
      ? "This is a DIALOGUE between named interlocutors. Each macro-section is a major beat in the conversation (a question, a reply, an objection, a concession, a turn). Sections should advance the dialogue, not restart it."
      : mode === "lecture"
      ? "This is a LECTURE. Each macro-section is a numbered teaching unit (definition, example, principle, application, objection-and-reply, exercise)."
      : "This is a long-form ESSAY. Each macro-section advances a single argumentative arc — never a self-contained mini-essay.";

  const system = `You are a structural architect for long-form philosophical writing in the voice of ${thinker}. Output ONLY valid JSON. No markdown fences, no preface, no commentary.`;

  const prompt = `User request: ${userPrompt}

Target length: ${targetWords} words across ${sectionCount} macro-sections (~${wordsPerSection} words each).
${modeNote}

Build a MACRO PLAN. The plan must guarantee a single coherent arc — not a heap of mini-essays. Each macro-section MUST do something different: advance the argument, introduce a distinction, raise an objection, reply to it, deploy a new example, push to a deeper level, or synthesize.

Output ONLY this JSON:
{
  "thesis": "One-sentence overall thesis the entire piece will establish (or, for dialogue, the central question being worked through).",
  "central_concepts": ["3-7 concepts that recur throughout"],
  "arc": "2-3 sentences describing the dramatic/argumentative arc from start to finish. Where does it begin, what is the turning point, where does it end?",
  "macro_sections": [
    {
      "title": "Concrete, distinctive title (no generic 'Introduction')",
      "role": "intro | thesis-statement | distinction | development | objection | reply | example | application | synthesis | conclusion | dialogue-opening | dialogue-challenge | dialogue-concession | dialogue-pivot | dialogue-resolution",
      "gist": "1-2 sentences on what this section uniquely contributes that no other section will",
      "word_target": ${wordsPerSection}
    }
  ]
}

Rules:
- Exactly ${sectionCount} macro_sections.
- No two sections may have overlapping gists. Every section must do something the others don't.
- Roles must vary — do not put 5 "development" sections in a row.
- Word targets must sum to approximately ${targetWords}.
- For dialogue mode, alternate roles to reflect turn-taking.`;

  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const raw = await chat(system, prompt, { maxTokens: 4000 });
      const j = extractJson(raw);
      if (!j) continue;
      const parsed = JSON.parse(j) as MacroPlan;
      if (parsed.macro_sections && parsed.macro_sections.length > 0) {
        return parsed;
      }
    } catch (e) {
      console.error(`Macro plan attempt ${attempt + 1} failed:`, e);
    }
  }

  // Fallback
  const sections: MacroPlan["macro_sections"] = [];
  for (let i = 0; i < sectionCount; i++) {
    sections.push({
      title: `Section ${i + 1}`,
      role: i === 0 ? "intro" : i === sectionCount - 1 ? "conclusion" : "development",
      gist: `Develops the argument at stage ${i + 1}`,
      word_target: wordsPerSection,
    });
  }
  return {
    thesis: userPrompt,
    central_concepts: [],
    arc: `An extended treatment of: ${userPrompt}`,
    macro_sections: sections,
  };
}

interface MicroPlanBatch {
  sections: {
    index: number;
    claims_to_make: string[];
    positions_to_use: string[];
    examples_to_use: string[];
    bridge_from_prior: string;
    bridge_to_next: string;
    must_not_repeat: string[];
  }[];
}

async function generateMicroPlan(
  thinker: string,
  macroPlan: MacroPlan,
  userPrompt: string,
  startIdx: number,
  endIdx: number
): Promise<MicroPlanBatch> {
  const slice = macroPlan.macro_sections
    .slice(startIdx, endIdx)
    .map((s, i) => `Section ${startIdx + i} — ${s.role} — "${s.title}": ${s.gist}`)
    .join("\n");

  const allTitles = macroPlan.macro_sections
    .map((s, i) => `${i}: ${s.title}`)
    .join("\n");

  const system = `You are a coherence engineer. Output ONLY valid JSON. No markdown fences.`;

  const prompt = `Topic: ${userPrompt}
Voice: ${thinker}
Overall thesis: ${macroPlan.thesis}
Central concepts: ${macroPlan.central_concepts.join(", ")}
Arc: ${macroPlan.arc}

ALL SECTIONS in the document (for cross-section anti-repetition awareness):
${allTitles}

For sections ${startIdx} through ${endIdx - 1}:
${slice}

For each section in this batch, produce a precise micro-plan that GUARANTEES it does NOT overlap with the other sections. Output ONLY this JSON:

{
  "sections": [
    {
      "index": ${startIdx},
      "claims_to_make": ["3-6 distinct claims this section must establish — phrased as concrete propositions, not topics. Each claim must be unique to this section."],
      "positions_to_use": ["3-5 short search queries (2-6 words each) for retrieving relevant philosophical positions from ${thinker}'s corpus. Each query targets a different angle."],
      "examples_to_use": ["1-3 concrete examples, cases, or thought experiments to deploy here. Must not be reused in other sections."],
      "bridge_from_prior": "1-2 sentences specifying how this section picks up exactly where the previous one left off — what unresolved tension, claim, or question it inherits.",
      "bridge_to_next": "1-2 sentences specifying what this section must leave open or set up so the next section has something to do.",
      "must_not_repeat": ["3-5 things from prior sections this section must NOT restate — phrased as the prior claim/example itself."]
    }
  ]
}

Hard rules:
- For section 0, bridge_from_prior = "Opening — establish the question/scene/problem."
- For the final section, bridge_to_next = "Close the arc — no further sections follow."
- claims_to_make for any two sections must not overlap.
- examples_to_use for any two sections must not overlap.`;

  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const raw = await chat(system, prompt, { maxTokens: 6000 });
      const j = extractJson(raw);
      if (!j) continue;
      const parsed = JSON.parse(j) as MicroPlanBatch;
      if (parsed.sections && parsed.sections.length > 0) return parsed;
    } catch (e) {
      console.error(`Micro plan batch ${startIdx}-${endIdx} attempt ${attempt + 1} failed:`, e);
    }
  }

  // Fallback
  const fallbackSections: MicroPlanBatch["sections"] = [];
  for (let i = startIdx; i < endIdx; i++) {
    const m = macroPlan.macro_sections[i];
    fallbackSections.push({
      index: i,
      claims_to_make: [m.gist],
      positions_to_use: [m.title],
      examples_to_use: [],
      bridge_from_prior: i === 0 ? "Opening." : `Continue from section ${i - 1}.`,
      bridge_to_next: i === macroPlan.macro_sections.length - 1 ? "Close." : `Set up section ${i + 1}.`,
      must_not_repeat: [],
    });
  }
  return { sections: fallbackSections };
}

export async function generateSkeleton(
  thinker: string,
  userPrompt: string,
  mode: string,
  targetWords: number,
  onProgress?: (msg: string) => void
): Promise<Skeleton> {
  onProgress?.(`Generating macro plan for ${targetWords}-word ${mode}...`);
  const macroPlan = await generateMacroPlan(thinker, userPrompt, mode, targetWords);
  onProgress?.(
    `Macro plan: thesis="${macroPlan.thesis.slice(0, 80)}..." with ${macroPlan.macro_sections.length} sections.`
  );

  // Build micro-plans in batches of 8 to keep prompts reasonable
  const total = macroPlan.macro_sections.length;
  const microPlansByIndex: Record<number, MicroPlanBatch["sections"][number]> = {};
  const BATCH = 8;
  for (let start = 0; start < total; start += BATCH) {
    const end = Math.min(total, start + BATCH);
    onProgress?.(`Building micro-plans for sections ${start}-${end - 1}...`);
    const batch = await generateMicroPlan(thinker, macroPlan, userPrompt, start, end);
    for (const s of batch.sections) {
      microPlansByIndex[s.index] = s;
    }
  }

  // Assemble full skeleton sections
  const sections: SkeletonSection[] = [];
  for (let i = 0; i < total; i++) {
    const macro = macroPlan.macro_sections[i];
    const micro = microPlansByIndex[i] || {
      index: i,
      claims_to_make: [macro.gist],
      positions_to_use: [macro.title],
      examples_to_use: [],
      bridge_from_prior: i === 0 ? "Opening." : "",
      bridge_to_next: i === total - 1 ? "Close." : "",
      must_not_repeat: [],
    };
    sections.push({
      index: i,
      title: macro.title,
      role: macro.role,
      word_target: macro.word_target,
      claims_to_make: micro.claims_to_make,
      positions_to_use: micro.positions_to_use,
      examples_to_use: micro.examples_to_use,
      bridge_from_prior: micro.bridge_from_prior,
      bridge_to_next: micro.bridge_to_next,
      must_not_repeat: micro.must_not_repeat,
    });
  }

  return {
    thesis: macroPlan.thesis,
    central_concepts: macroPlan.central_concepts || [],
    arc: macroPlan.arc,
    sections,
  };
}
