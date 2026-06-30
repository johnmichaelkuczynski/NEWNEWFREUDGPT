import { generateLongFormOutline } from "./generateLongFormOutline";
import { generateSection, SectionGenerationParams } from "./generateSection";

interface OutlineSection {
  title: string;
  description: string;
  estimatedWords: number;
  keyPoints: string[];
  subsections?: OutlineSection[];
}

export async function generateLongFormEssay(
  philosopher: string,
  topic: string
): Promise<string> {
  // Step 1: Generate the detailed outline
  const outline = await generateLongFormOutline(topic);

  // Step 2: Flatten the hierarchical outline into a sequential list
  const flatSections: Array<{
    title: string;
    description: string;
    estimatedWords: number;
    keyPoints: string[];
    nextHint: string;
  }> = [];

  function flatten(sections: OutlineSection[], nextHint: string = "") {
    for (let i = 0; i < sections.length; i++) {
      const section = sections[i];
      const nextSection = sections[i + 1];
      const hint = nextSection
        ? `${nextSection.title}: ${nextSection.description}`
        : "End of essay";

      flatSections.push({
        title: section.title,
        description: section.description,
        estimatedWords: section.estimatedWords,
        keyPoints: section.keyPoints,
        nextHint: hint,
      });

      if (section.subsections && section.subsections.length > 0) {
        flatten(section.subsections, hint);
      }
    }
  }

  flatten(outline.sections);

  // Step 3: Sequentially generate each section
  let fullEssay = "";
  let previousContent = "";

  for (let i = 0; i < flatSections.length; i++) {
    const sec = flatSections[i];

    const params: SectionGenerationParams = {
      philosopher,
      topic,
      outlineSummary: outline.summary,
      sectionTitle: sec.title,
      sectionDescription: sec.description,
      sectionKeyPoints: sec.keyPoints,
      estimatedWords: sec.estimatedWords,
      previousContent,
      nextSectionHint: sec.nextHint,
    };

    console.log(`Generating section ${i + 1}/${flatSections.length}: ${sec.title} (~${sec.estimatedWords} words)`);

    const sectionContent = await generateSection(params);

    fullEssay += sectionContent + "\n\n";
    previousContent += sectionContent + "\n\n";

    // Optional: keep previousContent trimmed to avoid context overflow
    if (previousContent.length > 30000) {
      previousContent = "Previous sections summary: " + outline.summary + "\n\n" + previousContent.slice(-25000);
    }
  }

  return fullEssay.trim();
}