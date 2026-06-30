import { generateLongFormEssay } from "./generateLongFormEssay";

export async function kuczynskiLongForm(topic: string): Promise<string> {
  console.log(`Kuczynski is beginning a long-form essay on: ${topic}`);

  const essay = await generateLongFormEssay("Kuczynski", topic);

  console.log("Kuczynski's long-form essay complete.");

  return essay.trim();
}

// Optional: Direct export for easy import in bot router
export default kuczynskiLongForm;