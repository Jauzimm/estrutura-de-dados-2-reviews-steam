import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import GameSelector from "../components/GameSelector";
import SummaryCard from "../components/SummaryCard";

export default function Home() {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/games")
      .then((res) => res.json())
      .then((data) => {
        setGames(data);

        if (data.length > 0) {
          setSelectedGame(data[0]);
        }
      });
  }, []);

  return (
    <div className="flex min-h-screen bg-[#0b1622]">
      <Sidebar />

      <main className="flex-1 p-10">
        <h1 className="text-5xl font-bold">
          Resumo de Reviews da Steam
        </h1>

        <GameSelector
          games={games}
          selectedGame={selectedGame}
          onChange={setSelectedGame}
        />

        {selectedGame && (
          <SummaryCard game={selectedGame} />
        )}
      </main>
    </div>
  );
}
