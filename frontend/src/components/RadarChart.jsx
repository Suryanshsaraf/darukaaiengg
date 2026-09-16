import React from 'react';

export default function RadarChart({ profile, recommendations }) {
  const categories = [
    { label: "Soil Carbon", key: "soc" },
    { label: "Infiltration", key: "water" },
    { label: "Mycorrhizal AMF", key: "fungi" },
    { label: "Biodiversity", key: "bio" },
    { label: "Ground Cover", key: "cover" },
    { label: "Microclimate", key: "micro" }
  ];

  const soc = profile?.soil_organic_carbon_pct || 0.4;
  const baseSoc = Math.min(1.0, soc / 3.0);
  const baseWater = (profile?.rainfall_annual_mm && profile.rainfall_annual_mm < 500) ? 0.35 : 0.55;
  const baseFungi = profile?.tillage_practice === "conventional_deep" ? 0.20 : 0.45;
  const baseBio = (profile?.land_use_type || "").includes("monoculture") ? 0.25 : 0.50;
  const baseCover = (profile?.vegetative_ground_cover_pct || 25.0) / 100.0;
  const baseMicro = (profile?.canopy_cover_pct || 0) < 10.0 ? 0.30 : 0.60;

  const baselineVals = [baseSoc, baseWater, baseFungi, baseBio, baseCover, baseMicro];
  const projectedVals = [
    Math.min(1.0, baseSoc * 1.70),
    Math.min(1.0, baseWater * 1.50),
    Math.min(1.0, baseFungi * 1.90),
    Math.min(1.0, baseBio * 1.75),
    Math.min(1.0, baseCover * 2.3),
    Math.min(1.0, baseMicro * 1.80)
  ];

  const width = 340;
  const height = 280;
  const center = { x: width / 2, y: height / 2 };
  const radius = 95;
  const angleStep = (Math.PI * 2) / categories.length;

  const getCoordinates = (value, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = radius * Math.max(0.1, Math.min(1.0, value));
    return {
      x: center.x + r * Math.cos(angle),
      y: center.y + r * Math.sin(angle)
    };
  };

  const baselinePoints = baselineVals.map((val, i) => {
    const pt = getCoordinates(val, i);
    return `${pt.x},${pt.y}`;
  }).join(' ');

  const projectedPoints = projectedVals.map((val, i) => {
    const pt = getCoordinates(val, i);
    return `${pt.x},${pt.y}`;
  }).join(' ');

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center shadow-lg h-full justify-between">
      <div className="w-full flex items-center justify-between mb-1 pb-2 border-b border-slate-800/80">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
          Multi-Metric Impact Polygon
        </span>
        <div className="flex items-center space-x-3 text-xs">
          <span className="flex items-center space-x-1 text-red-400 font-medium">
            <span className="w-2.5 h-0.5 bg-red-400 inline-block border-t border-dashed"></span>
            <span>Current Baseline</span>
          </span>
          <span className="flex items-center space-x-1 text-emerald-400 font-semibold">
            <span className="w-2.5 h-2.5 bg-emerald-500 rounded-sm inline-block shadow-sm"></span>
            <span>Projected (2-4 yrs)</span>
          </span>
        </div>
      </div>

      <div className="w-full flex justify-center items-center py-1">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full max-w-[320px] h-auto overflow-visible">
          {/* Grid circles */}
          {[0.25, 0.5, 0.75, 1.0].map((level, idx) => (
            <circle
              key={idx}
              cx={center.x}
              cy={center.y}
              r={radius * level}
              fill={idx === 3 ? "rgba(15, 23, 42, 0.6)" : "none"}
              stroke="#334155"
              strokeDasharray={level < 1.0 ? "2 2" : "none"}
              strokeWidth="1"
            />
          ))}

          {/* Category spokes & Labels */}
          {categories.map((cat, i) => {
            const outerPt = getCoordinates(1.0, i);
            const textPt = getCoordinates(1.26, i);
            return (
              <g key={i}>
                <line
                  x1={center.x}
                  y1={center.y}
                  x2={outerPt.x}
                  y2={outerPt.y}
                  stroke="#334155"
                  strokeWidth="1"
                />
                <text
                  x={textPt.x}
                  y={textPt.y}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fill="#94a3b8"
                  fontSize="10"
                  fontWeight="600"
                >
                  {cat.label}
                </text>
              </g>
            );
          })}

          {/* Projected Area */}
          <polygon
            points={projectedPoints}
            fill="rgba(16, 185, 129, 0.28)"
            stroke="#10b981"
            strokeWidth="2.5"
          />

          {/* Baseline Area */}
          <polygon
            points={baselinePoints}
            fill="none"
            stroke="#f87171"
            strokeWidth="2"
            strokeDasharray="4 3"
          />

          {/* Data points */}
          {projectedVals.map((val, i) => {
            const pt = getCoordinates(val, i);
            return <circle key={`p-${i}`} cx={pt.x} cy={pt.y} r="3.5" fill="#10b981" />;
          })}
          {baselineVals.map((val, i) => {
            const pt = getCoordinates(val, i);
            return <circle key={`b-${i}`} cx={pt.x} cy={pt.y} r="2.5" fill="#f87171" />;
          })}
        </svg>
      </div>

      <div className="w-full text-center pt-2 border-t border-slate-800/60 text-[11px] text-slate-400">
        Super-additive ecological synergy across edaphic, hydrologic, and biotic indicators
      </div>
    </div>
  );
}
