// src/components/WeeklyChart.jsx
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-surface-muted border border-surface-border rounded-xl px-4 py-3 text-sm">
      <p className="text-zinc-400 mb-1">{label}</p>
      <p className="font-mono text-brand-400">{payload[0].value.toLocaleString()} sessions</p>
    </div>
  )
}

export default function WeeklyChart({ data }) {
  const max = Math.max(...data.map(d => d.sessions))

  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 animate-slide-up animate-delay-300">
      <h3 className="text-sm font-semibold text-white mb-1">Weekly Activity</h3>
      <p className="text-xs text-zinc-500 mb-4">Sessions by day</p>
      <ResponsiveContainer width="100%" height={160}>
        <BarChart data={data} margin={{ top: 4, right: 4, left: -20, bottom: 0 }} barSize={28}>
          <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
          <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#71717a' }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 11, fill: '#71717a' }} axisLine={false} tickLine={false}
            tickFormatter={v => `${Math.round(v / 1000)}k`} />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(99,102,241,0.07)' }} />
          <Bar dataKey="sessions" radius={[4, 4, 0, 0]}>
            {data.map((entry, i) => (
              <Cell key={i}
                fill={entry.sessions === max ? '#6366f1' : '#3f3f46'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
