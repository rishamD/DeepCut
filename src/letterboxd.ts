export async function scrapeLetterboxd(username: string): Promise<string[]> {
  console.log("[scrape] Fetching Letterboxd for", username);
  const url = `https://letterboxd.com/${username}/films/`;
  const res = await fetch(url);
  console.log("[scrape] Letterboxd response", res.status, res.url);
  if (!res.ok) throw new Error("User not found or private");
  const html = await res.text();
  console.log("[scrape] HTML length", html.length);

  const slugs = new Set<string>();
  const re = /href="\/film\/([^"/]+)\//g;
  let m;
  while ((m = re.exec(html)) !== null) slugs.add(m[1]);
  const arr = Array.from(slugs).slice(0, 50);
  console.log("[scrape] Films found", arr.length, arr.slice(0, 3));
  return arr;
}