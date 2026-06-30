import { generateLongFormEssay } from "./generateLongFormEssay";

export async function freudLongForm(topic: string): Promise<string> {
  console.log(`Freud is beginning a long-form essay on: ${topic}`);

  const essay = await generateLongFormEssay("Freud", topic);

  console.log("Freud's long-form essay complete.");

  return essay.trim();
}

// Optional: Direct export for easy import in bot router
export default freudLongForm;