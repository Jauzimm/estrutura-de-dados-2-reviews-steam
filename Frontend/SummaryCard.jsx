export default function SummaryCard({ game }) {
  return (
    <div className="bg-[#10233a] rounded-3xl p-8">
      <h2 className="text-4xl font-bold">
        {game.name}
      </h2>

      <div className="mt-6">
        <h3 className="text-blue-400 text-xl">
          Resumo das Reviews
        </h3>

        <p className="mt-4 whitespace-pre-line">
          {game.summary}
        </p>
      </div>
    </div>
  );
}
