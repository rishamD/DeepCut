import React, { useState } from "react";
import { scrapeLetterboxd } from "./letterboxd";

function App() {
  const [user, setUser] = useState("");
  const [movies, setMovies] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("[App] Submit for", user);
    try {
      const watched = await scrapeLetterboxd(user);
      console.log("[App] Sending to API", watched);
      const res = await fetch("/api/suggest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ letterboxdUser: user, watched }),
      });
      const data = await res.json();
      console.log("[App] API response", data);
      setMovies(data.movies);
    } catch (err) {
      console.error("[App] Scrape error", err);
    }
  };

  return (
    <div style={{ padding: 32 }}>
      <h1>DeepCut</h1>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Letterboxd username"
          value={user}
          onChange={(e) => setUser(e.target.value)}
        />
        <button type="submit">Suggest movies</button>
      </form>
      <ul>
        {movies.map((m) => (
          <li key={m}>{m}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;