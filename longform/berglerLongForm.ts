import { generateLongFormEssay } from "./generateLongFormEssay";

export async function berglerLongForm(topic: string): Promise<string> {
  console.log(`Bergler is beginning a long-form essay on: ${topic}`);

  const essay = await generateLongFormEssay("Bergler", topic);

  console.log("Bergler's long-form essay complete.");

  return essay.trim();
}

export default berglerLongForm;
