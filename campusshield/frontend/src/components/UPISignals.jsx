// frontend/src/components/UPISignals.jsx

export default function UPISignals({ paymentScan }) {
  if (!paymentScan || !paymentScan.available) return null
  if (!paymentScan.upi_signals || paymentScan.upi_signals.length === 0) return null

  const dotStyle = {
    HIGH:   "bg-red-500",
    MEDIUM: "bg-amber-400",
    LOW:    "bg-gray-500",
  }

  const cardStyle = {
    HIGH:   "border-red-800 bg-red-950/30 text-red-300",
    MEDIUM: "border-amber-800 bg-amber-950/30 text-amber-300",
    LOW:    "border-gray-700 bg-gray-900 text-gray-300",
  }

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900/40 p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest">
          UPI Fraud Signals
        </h2>
        <span className="text-xs font-bold text-red-300 bg-red-950/50 border border-red-800 px-2.5 py-1 rounded-full">
          Payment Risk {paymentScan.payment_risk}/100
        </span>
      </div>

      <div className="space-y-3">
        {paymentScan.upi_signals.map((sig, i) => {
          const sev   = sig.severity || "LOW"
          const style = cardStyle[sev] || cardStyle.LOW
          const dot   = dotStyle[sev]  || dotStyle.LOW

          return (
            <div key={i} className={`rounded-xl border p-4 flex gap-3 items-start ${style}`}>
              <div className={`w-2.5 h-2.5 rounded-full mt-1 flex-shrink-0 ${dot}`} />
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-white mb-1">{sig.signal}</p>
                <p className="text-xs leading-relaxed opacity-80">{sig.detail}</p>
              </div>
              <span className={`text-xs font-bold flex-shrink-0 ${
                sev === "HIGH"   ? "text-red-400"   :
                sev === "MEDIUM" ? "text-amber-400" : "text-gray-400"
              }`}>
                {sev}
              </span>
            </div>
          )
        })}
      </div>

      {paymentScan.deep_scan_triggered && paymentScan.deep_scan_note && (
        <div className="mt-4 bg-orange-950/40 border border-orange-800 rounded-xl px-4 py-3">
          <p className="text-xs font-semibold text-orange-300 mb-1">
            Deep Scan Finding
          </p>
          <p className="text-xs text-orange-200 leading-relaxed">
            {paymentScan.deep_scan_note}
          </p>
        </div>
      )}
    </div>
  )
}