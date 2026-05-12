// src/components/MetricCard.jsx
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

function getChange(current, prev) {
  if (prev === null || typeof current === 'string') return null
  const pct = ((current - prev) / prev) * 100
  return pct.toFixed(1)
}

export default function MetricCard({ metric, delay = 0 }) {
  const change = getChange(metric.value, metric.prev)
  const isUp   = change !== null && parseFloat(change) > 0
  const isDown = change !== null && parseFloat(change) < 0

  return (
    <div
      className="animate-slide-up bg-surface-card border border-surface-border rounded-2xl p-5 flex flex-col gap-3"
      style={{ animationDelay: `${delay}ms` }}
    >
      <p className="text-xs font-medium text-zinc-500 uppercase tracking-widest">
        {metric.label}
      </p>

      <p className="text-3xl font-semibold text-white font-mono tracking-tight">
        {metric.prefix}
        {typeof metric.value === 'number'
          ? metric.value.toLocaleString()
          : metric.value}
        {metric.suffix}
      </p>

      {change !== null && (
        <div
          className={`flex items-center gap-1.5 text-sm font-medium ${
            isUp ? 'text-emerald-400' : isDown ? 'text-red-400' : 'text-zinc-500'
          }`}
        >
          {isUp   && <TrendingUp  size={14} />}
          {isDown && <TrendingDown size={14} />}
          {!isUp && !isDown && <Minus size={14} />}
          <span>{isUp ? '+' : ''}{change}% vs last month</span>
        </div>
      )}
    </div>
  )
}
