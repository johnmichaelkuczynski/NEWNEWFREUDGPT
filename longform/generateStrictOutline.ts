import { chat } from "./openai";

interface StrictOutlineSection {
  title: string;
  description: string;
  keyThemes: string[];
}

interface StrictOutline {
  summary: string;
  sections: StrictOutlineSection[];
}

export async function generateStrictOutline(
  fullText: string
): Promise<StrictOutline> {
  const system =
    "You are an expert document analyst. Output ONLY valid JSON. No extra text.";

  const truncatedText = fullText.slice(0, 50000);

  const prompt = `
Analyze this document and create a strict hierarchical outline.

DOCUMENT:
${truncatedText}

Output ONLY this exact JSON structure:
{
  "summary": "One paragraph summary of the entire document",
  "sections": [
    {
      "title": "Section title",
      "description": "2-3 sentence description of what this section covers",
      "keyThemes": ["theme1", "theme2", "theme3"]
    }
  ]
}

Create 5-20 sections that cover the entire document. Be exhaustive and precise.
`;

  const raw = await chat(system, prompt, { maxTokens: 8000 });

  try {
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
    return JSON.parse(raw);
  } catch (error) {
    console.error("Strict outline parsing failed:", error);
    return {
      summary: "Failed to parse document outline",
      sections: [
        {
          title: "Full Document",
          description: "The complete document content",
          keyThemes: ["document"],
        },
      ],
    };
  }
}
