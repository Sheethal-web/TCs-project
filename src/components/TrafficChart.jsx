// src/components/TrafficChart.jsx
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts'

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-surface-muted border border-surface-border rounded-xl px-4 py-3 text-sm">
      <p style={{ color: payload[0].payload.color }} className="font-medium">
        {payload[0].name}: {payload[0].value}%
      </p>
    </div>
  )
}

export default function TrafficChart({ data }) {
  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 animate-slide-up animate-delay-300 flex flex-col">
      <h3 className="text-sm font-semibold text-white mb-1">Traffic Sources</h3>
      <p className="text-xs text-zinc-500 mb-4">By channel</p>

      <div className="flex-1 flex items-center justify-center">
        <ResponsiveContainer width="100%" height={180}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" innerRadius={52} outerRadius={80}
              dataKey="value" paddingAngle={3} strokeWidth={0}>
              {data.map((entry, i) => (
                <Cell key={i} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <ul className="mt-2 space-y-2">
        {data.map((item) => (
          <li key={item.name} className="flex items-center justify-between text-xs">
            <span className="flex items-center gap-2 text-zinc-400">
              <span className="w-2 h-2 rounded-sm flex-shrink-0" style={{ background: item.color }} />
              {item.name}
            </span>
            <span className="font-mono font-medium text-white">{item.value}%</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
