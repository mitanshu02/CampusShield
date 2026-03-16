// frontend/src/pages/Home.jsx

import { useState } from "react";
import axios from "axios";
import URLInput from "../components/URLInput";
import RiskMeter from "../components/RiskMeter";
import SignalCards from "../components/SignalCards";
import DomainTimeline from "../components/DomainTimeline";
import AttackLabel from "../components/AttackLabel";
import ExplainerCard from "../components/ExplainerCard";
import DemoSimulator from "../components/DemoSimulator";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showDemo, setShowDemo] = useState(false);

  const handleScan = async (targetUrl) => {
    const scanTarget = targetUrl || url;
    if (!scanTarget.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const { data } = await axios.post(
        "http://localhost:8000/api/analyze-url",
        {
          url: scanTarget,
        },
      );
      setResult(data);
    } catch (e) {
      setError("Scan failed — make sure the backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };
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

        {showDemo && (
          <DemoSimulator
            onSelectScenario={(scenarioUrl) => setUrl(scenarioUrl)}
            onTriggerScan={(scenarioUrl) => handleScan(scenarioUrl)}
          />
        )}

        {/* URL Input */}
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

            {/* Animated risk meter */}
            <RiskMeter
              score={result.final_score}
              colour={result.risk_colour}
              label={result.risk_label}
            />

            {/* Domain age timeline — Upgrade 1 */}
            <DomainTimeline domainAgeSignal={result.signals?.domain_age} />

            {/* 4 signal cards */}
            <SignalCards signals={result.signals} />
            {/* Trust Explainer Card */}
            <ExplainerCard
              explanation={result.explanation}
              impersonationStatement={result.impersonation_statement}
              attackType={result.attack_type}
              riskScore={result.final_score}
            />
          </div>
        )}
      </main>
    </div>
  );
}
