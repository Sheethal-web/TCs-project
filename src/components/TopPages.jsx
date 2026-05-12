// src/components/TopPages.jsx
export default function TopPages({ data }) {
  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 animate-slide-up animate-delay-400">
      <h3 className="text-sm font-semibold text-white mb-1">Top Pages</h3>
      <p className="text-xs text-zinc-500 mb-4">By sessions this month</p>
      <ul className="space-y-1">
        {data.map((page, i) => {
          const isPositive = page.change.startsWith('+')
          return (
            <li key={page.path}
              className="flex items-center justify-between py-2.5 border-b border-surface-muted last:border-0">
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-zinc-600 w-4">{i + 1}</span>
                <span className="text-sm font-mono text-zinc-300">{page.path}</span>
              </div>
              <div className="flex items-center gap-4 text-right">
                <span className={`text-xs font-medium ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
                  {page.change}
                </span>
                <span className="text-sm font-mono text-white w-16 text-right">
                  {page.sessions.toLocaleString()}
                </span>
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
