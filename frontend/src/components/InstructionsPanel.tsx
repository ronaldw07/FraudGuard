// Author: Ronald Wen
export default function InstructionsPanel() {
  return (
    <div className="bg-navy-800 border border-slate-700 rounded-xl p-6 h-fit">
      <h2 className="text-lg font-semibold text-white mb-3">How This Works</h2>
      <ul className="text-slate-300 text-sm space-y-3 list-disc list-inside">
        <li>
          <span className="text-white font-medium">Time</span> and{' '}
          <span className="text-white font-medium">Amount</span> are real transaction values.
        </li>
        <li>
          <span className="text-white font-medium">V1–V10</span> are anonymized PCA features from
          the original dataset — any numbers work for a demo (try values between -3 and 3).
        </li>
        <li>
          Click <span className="text-white font-medium">Run Fraud Check</span> to score the
          transaction with the trained XGBoost model.
        </li>
        <li>
          Results show a <span className="text-white font-medium">risk badge</span>, a{' '}
          <span className="text-white font-medium">fraud probability</span>, and a{' '}
          <span className="text-white font-medium">SHAP chart</span> explaining which features
          drove the decision.
        </li>
        <li>
          Every prediction is saved to{' '}
          <span className="text-white font-medium">Recent Predictions</span> below.
        </li>
      </ul>
    </div>
  )
}
