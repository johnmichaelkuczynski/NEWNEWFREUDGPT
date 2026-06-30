import { generateLongFormEssay } from "./generateLongFormEssay";

export async function jungLongForm(topic: string): Promise<string> {
  console.log(`Jung is beginning a long-form essay on: ${topic}`);

  const essay = await generateLongFormEssay("Jung", topic);

  console.log("Jung's long-form essay complete.");

  return essay.trim();
}

export default jungLongForm;
