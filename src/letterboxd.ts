export async function scrapeLetterboxd(username: string): Promise<string[]> {
  // public “films” page (no auth needed)
  const url = `https://letterboxd.com/${username}/films/`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("User not found or private");
  const html = await res.text();

  // super-light regex for film slug  (/film/xyz/)
  const slugs = new Set<string>();
  const re = /href="\/film\/([^"/]+)\//g;
  let m;
  while ((m = re.exec(html)) !== null) slugs.add(m[1]);
  return Array.from(slugs).slice(0, 50); // cap at 50 for now
}