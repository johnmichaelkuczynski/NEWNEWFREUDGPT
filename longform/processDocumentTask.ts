import { chat } from "./openai";
import { extractDocumentSections } from "./extractDocumentSections";
import { deduce, searchPositions, formatPositionsForContext } from "./inference";

interface ProcessParams {
  philosopher?: string;
  fullText: string;
  task: string;
}

const THINKERS_WITH_INFERENCE = ["kuczynski", "nietzsche", "bergler"];

function isSummaryTask(task: string): boolean {
  const lower = task.toLowerCase();
  return lower.includes("summarize") || lower.includes("summary") || lower.includes("outline");
}

function isDialogueTask(task: string): boolean {
  const lower = task.toLowerCase();
  return lower.includes("dialogue") || lower.includes("dialog") || lower.includes("conversation");
}

function isRewriteTask(task: string): boolean {
  const lower = task.toLowerCase();
  return lower.includes("rewrite") || lower.includes("transform") || lower.includes("convert");
}

export async function processDocumentTask(params: ProcessParams): Promise<string> {
  const { philosopher, fullText, task } = params;
  const philosopherLower = philosopher?.toLowerCase() || "";

  const sections = extractDocumentSections(fullText);
  console.log(`Extracted ${sections.length} sections from document`);

  const isSummary = isSummaryTask(task);
  const isDialogue = isDialogueTask(task);
  
  const processedSections: string[] = [];

  for (let i = 0; i < sections.length; i++) {
    const section = sections[i];
    console.log(`Processing section ${i + 1}/${sections.length}: ${section.title}`);

    let system: string;
    let prompt: string;

    if (isSummary) {
      system = "You are a precise analyst. Provide faithful, accurate summaries that preserve the author's original arguments and structure. Do not add your own opinions or commentary.";
      
      prompt = `Task: ${task}

Section Title: ${section.title}

Section Text:
${section.text}

Provide a faithful summary of THIS section only. Preserve the author's key arguments, examples, and conclusions. Do not add external commentary or opinions. Output only the summary.`;

    } else if (isDialogue) {
      const voiceInstruction = philosopher 
        ? `Write as ${philosopher} engaging with the text.` 
        : "Write as a philosophical interlocutor.";
      
      system = voiceInstruction;
      
      prompt = `Task: ${task}

Section Title: ${section.title}

Section Text:
${section.text}

Transform this section into dialogue format. Preserve the core arguments and content.`;

    } else {
      let contextSection = "";
      
      if (philosopherLower && THINKERS_WITH_INFERENCE.includes(philosopherLower)) {
        const positions = await searchPositions(philosopherLower, section.title, 5);
        const positionsContext = formatPositionsForContext(positions);
        if (positionsContext) {
          contextSection += `\n\nRelevant positions:\n${positionsContext}`;
        }
        
        const chain = await deduce(philosopherLower, section.text.slice(0, 2000), 8);
        if (chain) {
          contextSection += `\n\nPhilosophical principles:\n${chain}`;
        }
      }
      
      system = philosopher 
        ? `You are ${philosopher}. Respond in your authentic voice.`
        : "You are a precise analyst.";
      
      prompt = `Task: ${task}

Section Title: ${section.title}

Section Text:
${section.text}
${contextSection}

Perform the task on this section. Output only the transformed content.`;
    }

    const result = await chat(system, prompt, { maxTokens: 2000 });
    
    processedSections.push(`## ${section.title}\n\n${result.trim()}`);
  }

  const output = processedSections.join("\n\n---\n\n");
  
  return output;
}
