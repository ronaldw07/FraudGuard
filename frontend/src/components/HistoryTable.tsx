// Author: Ronald Wen
import { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

interface HistoryItem {
  id: number
  timestamp: string
  amount: number
  fraud_probability: number
  risk_level: string
  prediction: boolean
}

const RISK_BADGE: Record<string, string> = {
  low: 'bg-green-900 text-green-300',
  medium: 'bg-yellow-900 text-yellow-300',
  high: 'bg-red-900 text-red-300',
}

interface Props {
  refreshKey: number
}

export default function HistoryTable({ refreshKey }: Props) {
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(false)
  const { token } = useAuth()

  useEffect(() => {
    if (!token) return
    setLoading(true)
    axios
      .get('/history', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setHistory(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [token, refreshKey])

  return (
    <div className="bg-navy-800 border border-slate-700 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-white mb-4">Recent Predictions</h2>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading...</p>
      ) : history.length === 0 ? (
        <p className="text-slate-400 text-sm">No predictions yet. Submit a transaction above.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left text-slate-400 font-medium pb-2 pr-4">Timestamp</th>
                <th className="text-right text-slate-400 font-medium pb-2 pr-4">Amount</th>
                <th className="text-right text-slate-400 font-medium pb-2 pr-4">Probability</th>
                <th className="text-center text-slate-400 font-medium pb-2 pr-4">Risk</th>
                <th className="text-center text-slate-400 font-medium pb-2">Verdict</th>
              </tr>
            </thead>
            <tbody>
              {history.map(item => (
                <tr key={item.id} className="border-b border-slate-800 hover:bg-navy-700 transition">
                  <td className="py-2 pr-4 text-slate-300">
                    {new Date(item.timestamp).toLocaleString()}
                  </td>
                  <td className="py-2 pr-4 text-right text-slate-300">
                    ${item.amount.toFixed(2)}
                  </td>
                  <td className="py-2 pr-4 text-right text-slate-300">
                    {(item.fraud_probability * 100).toFixed(1)}%
                  </td>
                  <td className="py-2 pr-4 text-center">
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${
                        RISK_BADGE[item.risk_level] ?? ''
                      }`}
                    >
                      {item.risk_level}
                    </span>
                  </td>
                  <td className="py-2 text-center">
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        item.prediction
                          ? 'bg-red-900 text-red-300'
                          : 'bg-green-900 text-green-300'
                      }`}
                    >
                      {item.prediction ? 'Fraud' : 'Legit'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
