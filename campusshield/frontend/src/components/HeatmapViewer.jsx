// frontend/src/components/HeatmapViewer.jsx
// placeholder — Feature 2 slots in here safely later

export default function HeatmapViewer({ visualScan }) {
  if (!visualScan || !visualScan.available) return null
  if (!visualScan.heatmap_url)             return null

  return (
    <div className="rounded-2xl border border-purple-900 bg-purple-950/20 p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest">
          Visual Brand Spoofing Analysis
        </h2>
        <span className="text-xs font-bold text-purple-300 bg-purple-950/50 border border-purple-800 px-2.5 py-1 rounded-full">
          {visualScan.visual_similarity}% match to {visualScan.detected_brand}
        </span>
      </div>
      <div className="rounded-xl overflow-hidden border border-gray-700">
        <p className="text-xs text-gray-500 px-3 py-2 bg-gray-800">
          Heatmap — red zones show tampered regions
        </p>
        <img
          src={`http://localhost:8000${visualScan.heatmap_url}`}
          alt="Visual heatmap"
          className="w-full"
        />
      </div>
      <p className="text-xs text-gray-600 mt-3 text-center">
        Red zones = regions that differ from the legitimate brand page
      </p>
    </div>
  )
}