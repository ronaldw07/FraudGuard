// Author: Ronald Wen
import { useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import type { PredictionResult } from '../pages/Dashboard'

const FIELDS: { name: string; label: string; placeholder: string; description: string }[] = [
  {
    name: 'Time',
    label: 'Time (sec)',
    placeholder: 'e.g. 50000',
    description: 'Seconds elapsed since the first transaction in the dataset — a technical timestamp, not a real clock time',
  },
  {
    name: 'Amount',
    label: 'Amount ($)',
    placeholder: 'e.g. 45.00',
    description: 'Transaction amount in USD',
  },
  ...Array.from({ length: 10 }, (_, i) => ({
    name: `V${i + 1}`,
    label: `V${i + 1}`,
    placeholder: '0',
    description: 'Anonymized signal — real-world meaning is not disclosed by the dataset (for cardholder privacy)',
  })),
]

type FormValues = Record<string, string>

const defaultValues: FormValues = Object.fromEntries(FIELDS.map(f => [f.name, '']))

const EXAMPLES: Record<'normal' | 'suspicious', FormValues> = {
  normal: {
    Time: '50000',
    Amount: '45.00',
    V1: '0', V2: '0', V3: '0', V4: '0', V5: '0',
    V6: '0', V7: '0', V8: '0', V9: '0', V10: '0',
  },
  suspicious: {
    Time: '2000',
    Amount: '9000',
    V1: '-3.5', V2: '2.8', V3: '-4.2', V4: '3.1', V5: '-2.9',
    V6: '0.5', V7: '-3.8', V8: '1.2', V9: '-2.5', V10: '-4.1',
  },
}

interface Props {
  onResult: (data: PredictionResult) => void
}

export default function TransactionForm({ onResult }: Props) {
  const [values, setValues] = useState<FormValues>(defaultValues)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { token } = useAuth()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setValues(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  function fillExample(kind: 'normal' | 'suspicious') {
    setValues(EXAMPLES[kind])
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const payload = Object.fromEntries(
        Object.entries(values).map(([k, v]) => [k, parseFloat(v) || 0])
      )
      const res = await axios.post('/predict', payload, {
        headers: { Authorization: `Bearer ${token}` },
      })
      onResult(res.data)
    } catch {
      setError('Prediction failed. Please check your inputs.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-navy-800 border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 gap-3 flex-wrap">
        <h2 className="text-lg font-semibold text-white">Analyze Transaction</h2>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => fillExample('normal')}
            className="text-xs px-3 py-1.5 rounded-lg border border-slate-600 text-slate-300 hover:border-green-500 hover:text-green-400 transition"
          >
            Try Normal Example
          </button>
          <button
            type="button"
            onClick={() => fillExample('suspicious')}
            className="text-xs px-3 py-1.5 rounded-lg border border-slate-600 text-slate-300 hover:border-red-500 hover:text-red-400 transition"
          >
            Try Suspicious Example
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          {FIELDS.map(field => (
            <div key={field.name}>
              <label className="block text-slate-300 text-xs font-medium mb-1">
                {field.label}
              </label>
              <input
                type="number"
                name={field.name}
                value={values[field.name]}
                onChange={handleChange}
                step="any"
                required
                title={field.description}
                placeholder={field.placeholder}
                className="w-full bg-navy-700 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm placeholder-slate-600 focus:outline-none focus:border-blue-500 transition"
              />
            </div>
          ))}
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold py-2.5 rounded-lg transition mt-2"
        >
          {loading ? 'Analyzing...' : 'Run Fraud Check'}
        </button>
      </form>
    </div>
  )
}
