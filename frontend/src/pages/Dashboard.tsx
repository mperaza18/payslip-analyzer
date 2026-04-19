const cards = [
  { title: 'Upload', description: 'Drag & drop payslip files', phase: 3 },
  { title: 'Summary', description: 'Annual & monthly KPIs', phase: 4 },
  { title: 'Charts', description: 'Stacked bar + pie breakdown', phase: 4 },
]

export default function Dashboard() {
  return (
    <main className="p-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {cards.map((card) => (
          <div
            key={card.title}
            className="rounded-lg border border-gray-700 bg-gray-800 p-6 opacity-50"
          >
            <h2 className="text-base font-medium text-white">{card.title}</h2>
            <p className="mt-1 text-sm text-gray-400">{card.description}</p>
            <p className="mt-3 text-xs text-gray-500">Coming in Phase {card.phase}</p>
          </div>
        ))}
      </div>
    </main>
  )
}
