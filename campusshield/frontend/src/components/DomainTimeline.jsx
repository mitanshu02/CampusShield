// frontend/src/components/DomainTimeline.jsx

export default function DomainTimeline({ domainAgeSignal }) {
  // Only render if we have both domain ages to compare
  if (
    !domainAgeSignal ||
    domainAgeSignal.suspicious_age_days === null ||
    domainAgeSignal.legitimate_age_days === null
  )
    return null;

  const susAge = domainAgeSignal.suspicious_age_days;
  const legAge = domainAgeSignal.legitimate_age_days;
  const susDomain = domainAgeSignal.suspicious_domain;
  const legDomain = domainAgeSignal.legitimate_domain;

  // Calculate bar widths as percentages relative to each other
  const total = susAge + legAge;
  const susWidth = Math.max((susAge / total) * 100, 2); // min 2% so bar is always visible
  const legWidth = Math.max((legAge / total) * 100, 2);

  const formatAge = (days) => {
    if (days < 30) return `${days} days old`;
    if (days < 365) return `${Math.floor(days / 30)} months old`;
    return `${Math.floor(days / 365)} years old`;
  };

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900/50 p-5">
      <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-4">
        Domain Age Comparison
      </h3>

      <div className="grid grid-cols-2 gap-4">
        {/* Suspicious domain */}
        <div>
          <p className="text-xs text-gray-400 mb-1 truncate">{susDomain}</p>
          <p className="text-sm font-bold text-red-400 mb-2">
            {formatAge(susAge)}
          </p>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-red-500 rounded-full"
              style={{ width: `${susWidth}%` }}
            />
          </div>
          <p className="text-xs text-red-400 mt-2">⚠ Suspicious domain</p>
        </div>

        {/* Legitimate domain */}
        <div>
          <p className="text-xs text-gray-400 mb-1 truncate">{legDomain}</p>
          <p className="text-sm font-bold text-green-400 mb-2">
            {formatAge(legAge)}
          </p>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 rounded-full"
              style={{ width: `${legWidth}%` }}
            />
          </div>
          <p className="text-xs text-green-400 mt-2">✓ Legitimate domain</p>
        </div>
      </div>

      <p className="text-xs text-gray-600 mt-4 text-center">
        A legitimate institution's domain is never just a few days old
      </p>
    </div>
  );
}
