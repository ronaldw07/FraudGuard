// Author: Ronald Wen
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
  ResponsiveContainer,
} from 'recharts'

interface Feature {
  feature: string
  shap_value: number
  direction: string
}

interface Props {
  features: Feature[]
}

export default function ShapChart({ features }: Props) {
  const data = features.map(f => ({
    feature: f.feature,
    value: Math.abs(f.shap_value),
    direction: f.direction,
    rawValue: f.shap_value,
  }))

  return (
    <div className="bg-navy-800 border border-slate-700 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-white mb-1">Feature Contributions</h2>
      <p className="text-slate-400 text-xs mb-4">Top 5 factors influencing this prediction</p>

      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="feature"
            tick={{ fill: '#cbd5e1', fontSize: 12 }}
            width={40}
          />
          <Tooltip
            contentStyle={{ backgroundColor: '#0d1526', border: '1px solid #334155', color: '#fff' }}
            formatter={(value: number, _: string, props: { payload?: { direction?: string; rawValue?: number } }) => [
              `${props.payload?.rawValue?.toFixed(4)} (${props.payload?.direction} fraud risk)`,
              'SHAP value',
            ]}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.direction === 'increases' ? '#ef4444' : '#22c55e'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="flex gap-4 mt-3">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-red-500" />
          <span className="text-slate-400 text-xs">Increases fraud risk</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-green-500" />
          <span className="text-slate-400 text-xs">Decreases fraud risk</span>
        </div>
      </div>
    </div>
  )
}
