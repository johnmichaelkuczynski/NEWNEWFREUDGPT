import { chat } from "./openai";
import { deduce, searchPositions, formatPositionsForContext } from "./inference";

export interface SectionGenerationParams {
  philosopher: string;
  topic: string;
  outlineSummary: string;
  sectionTitle: string;
  sectionDescription: string;
  sectionKeyPoints: string[];
  estimatedWords: number;
  previousContent: string;
  nextSectionHint?: string;
  conversationId?: string;
}

const THINKERS_WITH_INFERENCE = ["kuczynski", "nietzsche", "bergler"];

export async function generateSection(params: SectionGenerationParams): Promise<string> {
  const {
    philosopher,
    topic,
    outlineSummary,
    sectionTitle,
    sectionDescription,
    sectionKeyPoints,
    estimatedWords,
    previousContent,
    nextSectionHint = "",
  } = params;

  const philosopherLower = philosopher.toLowerCase();

  const positions = await searchPositions(philosopherLower, `${sectionTitle} ${sectionDescription}`, 8);
  const positionsContext = formatPositionsForContext(positions);

  let inferenceChain = "";
  if (THINKERS_WITH_INFERENCE.includes(philosopherLower)) {
    const contextForDeduction = `${sectionTitle} ${sectionDescription} ${sectionKeyPoints.join(" ")}`;
    inferenceChain = await deduce(philosopherLower, contextForDeduction, 10);
  }

  const system = `You are ${philosopher}. Write exclusively in your own authentic philosophical voice, style, and perspective. Use your characteristic language, concepts, and tone. Never break character.`;

  let contextSection = "";
  if (positionsContext) {
    contextSection += `\n\nRelevant positions from your works:\n${positionsContext}`;
  }
  if (inferenceChain) {
    contextSection += `\n\nPhilosophical principles to apply:\n${inferenceChain}`;
  }

  const prompt = `
Overall topic: ${topic}
Overall essay summary: ${outlineSummary}
${contextSection}

Previous content generated so far:
${previousContent.slice(-10000)}

Current section to write:
Title: ${sectionTitle}
Description: ${sectionDescription}
Key points to cover: ${sectionKeyPoints.join("\n- ")}
Estimated length: ~${estimatedWords} words

Next section (for continuity): ${nextSectionHint}

Write ONLY the content for this section. Do not add headings, section titles, or any meta-commentary. Continue seamlessly from the previous content. Maintain philosophical depth and coherence. Draw from the relevant positions and principles provided above.
`;

  const raw = await chat(system, prompt, { maxTokens: estimatedWords * 1.5 + 500 });

  return raw.trim();
}
