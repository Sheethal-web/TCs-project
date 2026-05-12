// src/components/ProgressStats.jsx
export default function ProgressStats({ data }) {
  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 animate-slide-up animate-delay-400">
      <h3 className="text-sm font-semibold text-white mb-1">Engagement</h3>
      <p className="text-xs text-zinc-500 mb-5">Key behavioral metrics</p>
      <ul className="space-y-5">
        {data.map(stat => (
          <li key={stat.label}>
            <div className="flex justify-between text-xs mb-2">
              <span className="text-zinc-400">{stat.label}</span>
              <span className="font-mono font-medium text-white">{stat.value}%</span>
            </div>
            <div className="h-1.5 bg-surface-muted rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700 ease-out"
                style={{ width: `${stat.value}%`, background: stat.color }}
              />
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
