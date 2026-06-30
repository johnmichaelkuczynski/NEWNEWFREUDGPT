import { generateLongFormEssay } from "./generateLongFormEssay";

export async function humeLongForm(topic: string): Promise<string> {
  console.log(`Hume is beginning a long-form essay on: ${topic}`);

  const essay = await generateLongFormEssay("Hume", topic);

  console.log("Hume's long-form essay complete.");

  return essay.trim();
}

export default humeLongForm;
