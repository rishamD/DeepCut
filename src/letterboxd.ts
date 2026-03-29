export async function scrapeLetterboxd(username: string): Promise<string[]> {
  const url = `https://abc123.your-subdomain.workers.dev?user=${encodeURIComponent(username)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("scrape failed");
  const { slugs } = await res.json();
  return slugs;
}