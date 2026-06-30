import { generateLongFormEssay } from "./generateLongFormEssay";

export async function nietzscheLongForm(topic: string): Promise<string> {
  console.log(`Nietzsche is beginning a long-form essay on: ${topic}`);

  const essay = await generateLongFormEssay("Nietzsche", topic);

  console.log("Nietzsche's long-form essay complete.");

  return essay.trim();
}

export default nietzscheLongForm;
