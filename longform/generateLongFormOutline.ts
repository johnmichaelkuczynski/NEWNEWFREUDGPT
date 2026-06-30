import { chat } from "./openai";

export interface LongFormOutline {
  summary: string;
  estimatedWordCount: number;
  sections: {
    title: string;
    description: string;
    estimatedWords: number;
    keyPoints: string[];
    subsections?: LongFormOutline["sections"];
  }[];
}

function cleanJsonString(raw: string): string {
  let cleaned = raw.trim();
  
  cleaned = cleaned.replace(/```json\s*/gi, "").replace(/```\s*/g, "");
  
  cleaned = cleaned.replace(/,(\s*[}\]])/g, "$1");
  
  cleaned = cleaned.replace(/\[\s*\.\.\.\s*recursive if needed\s*\.\.\.\s*\]/gi, "[]");
  cleaned = cleaned.replace(/\[\s*\.\.\.\s*\]/g, "[]");
  cleaned = cleaned.replace(/"\.\.\.\s*recursive.*?"/gi, '""');
  
  return cleaned;
}

function extractJson(raw: string): string | null {
  const cleaned = cleanJsonString(raw);
  
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

export async function generateLongFormOutline(topic: string): Promise<LongFormOutline> {
  const system = "You are an expert long-form writer. Output ONLY valid JSON. No markdown, no code blocks, no explanations before or after.";

  const prompt = `
Topic: ${topic}

Generate a detailed, hierarchical outline for a book-length essay (~15,000 words) on this topic.
Plan for depth and coherence. Use sections and subsections.
Every section/subsection must have realistic estimated word counts that sum to approximately 15,000.

Output ONLY this exact JSON structure with no other text:
{
  "summary": "one-paragraph overall summary of the planned essay",
  "estimatedWordCount": 15000,
  "sections": [
    {
      "title": "Section Title",
      "description": "2-4 sentence description of what this section covers",
      "estimatedWords": 1200,
      "keyPoints": ["point 1", "point 2", "point 3"],
      "subsections": []
    }
  ]
}

CRITICAL: Output valid JSON only. No trailing commas. No ellipses. Empty arrays for subsections if none.
`;

  for (let attempt = 0; attempt < 2; attempt++) {
    const raw = await chat(system, prompt, { maxTokens: 8000 });

    try {
      const jsonStr = extractJson(raw);
      if (jsonStr) {
        const parsed = JSON.parse(jsonStr);
        if (parsed.sections && parsed.sections.length > 0) {
          return parsed;
        }
      }
    } catch (error) {
      console.error(`Outline parsing attempt ${attempt + 1} failed:`, error);
    }
  }

  console.log("Falling back to simple outline structure");
  return {
    summary: `A comprehensive philosophical exploration of: ${topic}`,
    estimatedWordCount: 15000,
    sections: [
      {
        title: "Introduction and Historical Context",
        description: "Setting the philosophical stage and tracing the historical development of ideas related to this topic.",
        estimatedWords: 2000,
        keyPoints: ["Historical origins", "Key thinkers", "Central questions"],
        subsections: [],
      },
      {
        title: "Core Theoretical Framework",
        description: "Examining the fundamental theoretical structures and conceptual foundations.",
        estimatedWords: 3000,
        keyPoints: ["Primary concepts", "Theoretical relationships", "Foundational principles"],
        subsections: [],
      },
      {
        title: "Critical Analysis and Implications",
        description: "Deep analysis of the implications and critical examination of the core ideas.",
        estimatedWords: 3500,
        keyPoints: ["Critical perspectives", "Practical implications", "Theoretical challenges"],
        subsections: [],
      },
      {
        title: "Contemporary Applications",
        description: "Exploring how these philosophical insights apply to modern contexts and current debates.",
        estimatedWords: 3000,
        keyPoints: ["Modern relevance", "Current applications", "Contemporary debates"],
        subsections: [],
      },
      {
        title: "Synthesis and Conclusion",
        description: "Bringing together the threads of argument and offering final reflections.",
        estimatedWords: 3500,
        keyPoints: ["Integration of ideas", "Final synthesis", "Future directions"],
        subsections: [],
      },
    ],
  };
}
