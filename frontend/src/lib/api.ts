export type Document = {
  id: number;
  title: string;
  text: string;
};

export type SearchResult = {
  document: Document;
  score: number;
};

export async function search(
  query: string,
  topK: number = 5
): Promise<SearchResult[]> {
  const response = await fetch("http://127.0.0.1:8000/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query,
      top_k: topK
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Search request failed (${response.status}): ${errorText}`
    );
  }

  return response.json();
}
