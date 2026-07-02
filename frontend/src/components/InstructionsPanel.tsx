// Author: Ronald Wen
export default function InstructionsPanel() {
  return (
    <div className="bg-navy-800 border border-slate-700 rounded-xl p-6 h-fit space-y-5">
      <div>
        <h2 className="text-lg font-semibold text-white mb-2">What is this?</h2>
        <p className="text-slate-300 text-sm leading-relaxed">
          This mimics what happens behind the scenes when you swipe a credit card. Every
          transaction gets scored in real time by a machine learning model trained on real,
          anonymized credit card data — and this dashboard shows you exactly what it decides and
          why.
        </p>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-white mb-2">The fields, explained</h3>
        <ul className="text-slate-300 text-sm space-y-2.5">
          <li>
            <span className="text-white font-medium">Time</span> — not a real clock time. It's a
            technical counter (seconds since the dataset's first recorded transaction). Any
            number works.
          </li>
          <li>
            <span className="text-white font-medium">Amount</span> — the dollar value of the
            transaction. This one's real and intuitive.
          </li>
          <li>
            <span className="text-white font-medium">V1–V10</span> — anonymized signals (card
            usage patterns, merchant info, etc.) that banks intentionally scramble to protect
            cardholder privacy. Nobody, not even the dataset's creators, discloses what each one
            literally means — but the model still learned which patterns correlate with fraud.
            Values further from 0 tend to look more unusual to the model.
          </li>
        </ul>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-white mb-2">Fastest way to try it</h3>
        <p className="text-slate-300 text-sm leading-relaxed">
          Skip typing numbers — click <span className="text-white font-medium">"Try Normal
          Example"</span> or <span className="text-white font-medium">"Try Suspicious
          Example"</span> above the form, then hit <span className="text-white font-medium">Run
          Fraud Check</span>. Compare the two to see the model actually tell them apart.
        </p>
      </div>
    </div>
  )
}
