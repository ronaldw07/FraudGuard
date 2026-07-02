// Author: Ronald Wen
import { useState } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import type { PredictionResult } from '../pages/Dashboard'

const FIELDS: { name: string; label: string; description: string }[] = [
  { name: 'Time', label: 'Time', description: 'Seconds elapsed since the first transaction in the dataset' },
  { name: 'Amount', label: 'Amount ($)', description: 'Transaction amount in USD' },
  ...Array.from({ length: 10 }, (_, i) => ({
    name: `V${i + 1}`,
    label: `V${i + 1}`,
    description: 'Anonymized PCA component — real-world meaning is not disclosed by the dataset',
  })),
]

type FormValues = Record<string, string>

const defaultValues: FormValues = Object.fromEntries(FIELDS.map(f => [f.name, '']))

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
      <h2 className="text-lg font-semibold text-white mb-4">Analyze Transaction</h2>

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
                placeholder={field.description}
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
