// frontend/src/components/HeatmapViewer.jsx

export default function HeatmapViewer({ visualScan }) {
  if (!visualScan || !visualScan.available) return null;
  if (!visualScan.spoofing_detected) return null;

  const panels = [
    {
      label: "Suspicious Page",
      img: visualScan.suspect_image,
      note: "Page being scanned",
      border: "border-red-800",
    },
    {
      label: `Real ${visualScan.detected_brand || "Brand"}`,
      img: visualScan.template_image,
      note: "Known legitimate page",
      border: "border-green-800",
    },
    {
      label: "Difference Heatmap",
      img: visualScan.heatmap_image,
      note: "Red zones = tampered regions",
      border: "border-orange-800",
    },
  ];

  return (
    <div className="rounded-2xl border border-purple-900 bg-purple-950/20 p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest">
          Visual Brand Spoofing Analysis
        </h2>
        <span className="text-xs font-bold text-red-300 bg-red-950/50 border border-red-800 px-2.5 py-1 rounded-full">
          {visualScan.visual_similarity}% match to {visualScan.detected_brand}
        </span>
      </div>

      {/* Three panel comparison */}
      <div className="grid grid-cols-3 gap-3">
        {panels.map(({ label, img, note, border }) => (
          <div key={label}>
            <div
              className={`rounded-xl overflow-hidden border ${border} bg-gray-900 aspect-video`}
            >
              {img ? (
                <img
                  src={`data:image/png;base64,${img}`}
                  alt={label}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-600 text-xs">
                  No image
                </div>
              )}
            </div>
            <p className="text-xs font-medium text-gray-300 text-center mt-2">
              {label}
            </p>
            <p className="text-xs text-gray-600 text-center">{note}</p>
          </div>
        ))}
      </div>

      {/* Caption */}
      <p className="text-xs text-red-400 mt-4 text-center">
        Red zones highlight regions where the suspicious page was modified from
        the real design
      </p>
    </div>
  );
}
