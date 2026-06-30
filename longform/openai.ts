import Anthropic from "@anthropic-ai/sdk";

// Prefer the user's own ANTHROPIC_API_KEY when provided.
// Falls back to Replit AI Integrations (no user API key required) if no own key is set.
const anthropic = process.env.ANTHROPIC_API_KEY
  ? new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
  : process.env.AI_INTEGRATIONS_ANTHROPIC_API_KEY &&
      process.env.AI_INTEGRATIONS_ANTHROPIC_BASE_URL
    ? new Anthropic({
        apiKey: process.env.AI_INTEGRATIONS_ANTHROPIC_API_KEY,
        baseURL: process.env.AI_INTEGRATIONS_ANTHROPIC_BASE_URL,
      })
    : new Anthropic();

interface ChatOptions {
  maxTokens?: number;
  model?: string;
}

export async function chat(
  system: string,
  prompt: string,
  options: ChatOptions = {}
): Promise<string> {
  const { maxTokens = 4096, model = "claude-sonnet-4-5-20250929" } = options;

  const response = await anthropic.messages.create({
    model,
    max_tokens: maxTokens,
    system,
    messages: [{ role: "user", content: prompt }],
  });

  const textBlock = response.content.find((block) => block.type === "text");
  return textBlock ? textBlock.text : "";
}
