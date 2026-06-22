export default function GameSelector({
  games,
  selectedGame,
  onChange,
}) {
  return (
    <select
      className="w-full p-4 rounded-xl"
      value={selectedGame?.appid || ""}
      onChange={(e) => {
        const game = games.find(
          (g) => String(g.appid) === e.target.value
        );

        onChange(game);
      }}
    >
      {games.map((game) => (
        <option
          key={game.appid}
          value={game.appid}
        >
          {game.name}
        </option>
      ))}
    </select>
  );
}
