export type SearchQuery = {
  query: string;
  timestamp: number;
};

export function addToHistory(
  history: SearchQuery[],
  query: string,
  maxSize: number = 5
): SearchQuery[] {
  if (history.length > 0 && history[0].query === query) {
    return history;
  }

  return [
    { query, timestamp: Date.now() },
    ...history
  ].slice(0, maxSize);
}

export function getRecentQueries(
  history: SearchQuery[]
): string[] {
  return history.map(h => h.query);
}
