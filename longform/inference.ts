const FLASK_URL = "http://localhost:5000";

export interface Position {
  id: string;
  text: string;
  title: string;
  domain: string;
  similarity: number;
}

export interface DeduceResult {
  success: boolean;
  thinker: string;
  rulesCount: number;
  chain: string;
}

export interface SearchResult {
  success: boolean;
  thinker: string;
  count: number;
  positions: Position[];
}

export async function deduce(thinker: string, text: string, maxRules = 15): Promise<string> {
  try {
    const response = await fetch(`${FLASK_URL}/api/inference/deduce`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ thinker, text, maxRules }),
    });

    const data: DeduceResult = await response.json();
    return data.chain || "";
  } catch (error) {
    console.error(`Inference deduce error for ${thinker}:`, error);
    return "";
  }
}

export async function searchPositions(
  thinker: string,
  query: string,
  limit = 10
): Promise<Position[]> {
  try {
    const response = await fetch(`${FLASK_URL}/api/inference/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ thinker, query, limit }),
    });

    const data: SearchResult = await response.json();
    return data.positions || [];
  } catch (error) {
    console.error(`Semantic search error for ${thinker}:`, error);
    return [];
  }
}

export function formatPositionsForContext(positions: Position[]): string {
  if (!positions.length) return "";

  return positions
    .map((p, i) => {
      const title = p.title ? `"${p.title}"` : "";
      return `[Source ${i + 1}${title ? ` - ${title}` : ""}]\n${p.text}`;
    })
    .join("\n\n");
}
