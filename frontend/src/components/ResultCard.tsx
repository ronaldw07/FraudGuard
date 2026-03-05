// Author: Ronald Wen
import type { PredictionResult } from '../pages/Dashboard'

const RISK_STYLES: Record<string, string> = {
  low: 'bg-green-900 text-green-300 border-green-700',
  medium: 'bg-yellow-900 text-yellow-300 border-yellow-700',
  high: 'bg-red-900 text-red-300 border-red-700',
}

interface Props {
  result: PredictionResult
}

export default function ResultCard({ result }: Props) {
  const pct = (result.fraud_probability * 100).toFixed(1)
  const riskStyle = RISK_STYLES[result.risk_level] ?? RISK_STYLES.medium

  return (
    <div className="bg-navy-800 border border-slate-700 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-white mb-4">Analysis Result</h2>

      <div className="flex items-center gap-6 mb-4">
        <div className="text-center">
          <p className="text-4xl font-bold text-white">{pct}%</p>
          <p className="text-slate-400 text-xs mt-1">Fraud Probability</p>
        </div>

        <div className="flex flex-col gap-2">
          <span
            className={`px-3 py-1 rounded-full text-sm font-semibold border capitalize ${riskStyle}`}
          >
            {result.risk_level} Risk
          </span>

          <span
            className={`px-3 py-1 rounded-full text-sm font-semibold border ${
              result.prediction
                ? 'bg-red-900 text-red-300 border-red-700'
                : 'bg-green-900 text-green-300 border-green-700'
            }`}
          >
            {result.prediction ? 'Fraudulent' : 'Legitimate'}
          </span>
        </div>
      </div>

      <div className="w-full bg-slate-700 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all ${
            result.risk_level === 'low'
              ? 'bg-green-500'
              : result.risk_level === 'medium'
              ? 'bg-yellow-500'
              : 'bg-red-500'
          }`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
