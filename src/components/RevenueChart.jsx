// src/components/RevenueChart.jsx
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-surface-muted border border-surface-border rounded-xl px-4 py-3 text-sm shadow-xl">
      <p className="text-zinc-400 mb-2 font-medium">{label}</p>
      {payload.map(p => (
        <p key={p.dataKey} className="font-mono" style={{ color: p.color }}>
          {p.name === 'revenue' ? '$' : ''}{p.value.toLocaleString()}
          {p.name === 'users' ? ' users' : ''}
        </p>
      ))}
    </div>
  )
}

export default function RevenueChart({ data }) {
  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 animate-slide-up animate-delay-200">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-sm font-semibold text-white">Revenue &amp; Users</h3>
          <p className="text-xs text-zinc-500 mt-0.5">12-month overview</p>
        </div>
        <div className="flex gap-4 text-xs text-zinc-500">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-sm bg-brand-500 inline-block" />
            Revenue
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-sm bg-cyan-400 inline-block" />
            Users
          </span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={240}>
        <AreaChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
          <defs>
            <linearGradient id="gradRevenue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#6366f1" stopOpacity={0.25} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="gradUsers" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#22d3ee" stopOpacity={0.20} />
              <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
          <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#71717a' }} axisLine={false} tickLine={false} />
          <YAxis yAxisId="rev" tick={{ fontSize: 11, fill: '#71717a' }} axisLine={false} tickLine={false}
            tickFormatter={v => `$${Math.round(v / 1000)}k`} />
          <YAxis yAxisId="usr" orientation="right" tick={{ fontSize: 11, fill: '#71717a' }}
            axisLine={false} tickLine={false} tickFormatter={v => `${Math.round(v / 1000)}k`} />
          <Tooltip content={<CustomTooltip />} />
          <Area yAxisId="rev" type="monotone" dataKey="revenue" name="revenue"
            stroke="#6366f1" strokeWidth={2} fill="url(#gradRevenue)" dot={false} activeDot={{ r: 4, fill: '#6366f1' }} />
          <Area yAxisId="usr" type="monotone" dataKey="users" name="users"
            stroke="#22d3ee" strokeWidth={2} fill="url(#gradUsers)" dot={false} activeDot={{ r: 4, fill: '#22d3ee' }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
