// frontend/src/pages/Home.jsx

import { useState }    from "react"
import { scanURL }     from "../services/api"
import URLInput        from "../components/URLInput"
import RiskMeter       from "../components/RiskMeter"
import SignalCards     from "../components/SignalCards"
import DomainTimeline  from "../components/DomainTimeline"
import AttackLabel     from "../components/AttackLabel"
import ExplainerCard   from "../components/ExplainerCard"
import DemoSimulator   from "../components/DemoSimulator"
import UPISignals      from "../components/UPISignals"
import HeatmapViewer   from "../components/HeatmapViewer"
import LiteracyScore, { updateLiteracyScore } from "../components/LiteracyScore"

function getRiskColour(score) {
  if (score >= 70) return "red"
  if (score >= 40) return "amber"
  return "green"
}

export default function Home() {
  const [url,      setUrl]      = useState("")
  const [loading,  setLoading]  = useState(false)
  const [result,   setResult]   = useState(null)
  const [error,    setError]    = useState(null)
  const [showDemo, setShowDemo] = useState(false)

  const handleScan = async (targetUrl) => {
    const scanTarget = (targetUrl || url).trim()
    if (!scanTarget) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await scanURL(scanTarget)
      setResult(data)
      updateLiteracyScore(data.overall_risk, data.attack_type)
    } catch (e) {
      setError("Scan failed — make sure the backend is running on port 8000.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center gap-3">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-sm font-bold">
          CS
        </div>
        <span className="text-lg font-semibold">CampusShield</span>
        <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded-full">
          AI Fraud Intelligence
        </span>
        <button
          onClick={() => setShowDemo(!showDemo)}
          className="text-xs text-gray-400 border border-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-800 transition"
        >
          {showDemo ? "Hide Demo" : "Demo Mode"}
        </button>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-10 space-y-8">

        {/* Hero */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">
            Is this URL safe?
          </h1>
          <p className="text-gray-400 text-sm">
            Paste any URL to check for phishing, typosquatting, and UPI fraud.
          </p>
        </div>

        {/* Demo simulator */}
        {showDemo && (
          <DemoSimulator
            onSelectScenario={(scenarioUrl) => setUrl(scenarioUrl)}
            onTriggerScan={(scenarioUrl)    => handleScan(scenarioUrl)}
          />
        )}

        {/* URL input */}
        <URLInput
          url={url}
          setUrl={setUrl}
          onScan={() => handleScan()}
          loading={loading}
        />

        {/* Error */}
        {error && (
          <div className="bg-red-900/30 border border-red-700 rounded-xl p-4 text-red-300 text-sm">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-6">

            {/* Attack label — Upgrade 3 */}
            <AttackLabel attackType={result.attack_type} />

            {/* Risk meter */}
            <RiskMeter
              score={result.overall_risk}
              colour={getRiskColour(result.overall_risk)}
              label={result.verdict}
            />

            {/* Domain age timeline — Upgrade 1 */}
            <DomainTimeline
              domainAgeSignal={result.url_scan?.signals?.domain_age}
            />

            {/* 4 URL signal cards */}
            <SignalCards signals={result.url_scan?.signals} />

            {/* UPI fraud signals — Feature 3 */}
            <UPISignals paymentScan={result.payment_scan} />

            {/* Visual heatmap — Feature 2 — renders only when available */}
            <HeatmapViewer visualScan={result.visual_scan} />

            {/* Trust explainer card — Feature 4 */}
            <ExplainerCard
              explanation={result.explanation}
              impersonationStatement={result.impersonation_statement}
              attackType={result.attack_type}
              riskScore={result.overall_risk}
            />

            {/* Literacy score — Feature 5A */}
            <LiteracyScore />

          </div>
        )}

      </main>
    </div>
  )
}
