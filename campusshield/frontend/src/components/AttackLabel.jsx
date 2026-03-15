// frontend/src/components/AttackLabel.jsx

export default function AttackLabel({ attackType }) {
  if (!attackType || attackType === "Safe") return null;

  // High severity patterns → red, medium → amber
  const highSeverity = [
    "Fee Portal Impersonation",
    "UPI Collect Fraud",
    "Visual Phishing",
    "Domain Spoofing",
    "Semester Timing Phish",
  ];

  const isHigh = highSeverity.some((pattern) =>
    attackType.toLowerCase().includes(pattern.toLowerCase()),
  );

  const colour = isHigh
    ? "bg-red-950/50 border-red-700 text-red-300"
    : "bg-amber-950/50 border-amber-700 text-amber-300";

  const dot = isHigh ? "bg-red-500" : "bg-amber-400";

  return (
    <div className="flex items-center gap-2">
      <span
        className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-semibold ${colour}`}
      >
        <span className={`w-2 h-2 rounded-full ${dot}`} />
        {attackType}
      </span>
    </div>
  );
}
