// Author: Ronald Wen
import { useState } from 'react'
import Navbar from '../components/Navbar'
import TransactionForm from '../components/TransactionForm'
import ResultCard from '../components/ResultCard'
import ShapChart from '../components/ShapChart'
import HistoryTable from '../components/HistoryTable'

export interface PredictionResult {
  fraud_probability: number
  risk_level: string
  prediction: boolean
  shap_values: { feature: string; shap_value: number; direction: string }[]
}

export default function Dashboard() {
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [historyRefresh, setHistoryRefresh] = useState(0)

  function handleResult(data: PredictionResult) {
    setResult(data)
    setHistoryRefresh(n => n + 1)
  }

  return (
    <div className="min-h-screen bg-navy-900">
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
          <TransactionForm onResult={handleResult} />

          {result && (
            <div className="flex flex-col gap-6">
              <ResultCard result={result} />
              <ShapChart features={result.shap_values} />
            </div>
          )}
        </div>

        <HistoryTable refreshKey={historyRefresh} />
      </main>
    </div>
  )
}
