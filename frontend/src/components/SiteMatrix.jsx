import React, { useState } from 'react';
import { 
  Sliders, MapPin, Sparkles, RefreshCw, Layers, 
  HelpCircle, ShieldCheck, CheckCircle2, ChevronRight 
} from 'lucide-react';
import RadarChart from './RadarChart';

export default function SiteMatrix({ 
  onDiagnose, 
  onEnrichCoordinates, 
  activePlan, 
  isLaymanMode 
}) {
  const [lat, setLat] = useState(31.5);
  const [lon, setLon] = useState(-102.3);
  const [soc, setSoc] = useState(0.3);
  const [ph, setPh] = useState(7.2);
  const [bulkDensity, setBulkDensity] = useState(1.52);
  const [groundCover, setGroundCover] = useState(25);
  const [rainfall, setRainfall] = useState(320);
  const [climate, setClimate] = useState('semi_arid');
  const [landUse, setLandUse] = useState('monoculture_cropland');
  const [crop, setCrop] = useState('monoculture wheat');
  const [tillage, setTillage] = useState('conventional_deep');
  const [pesticides, setPesticides] = useState(2.0);
  const [isEnriching, setIsEnriching] = useState(false);

  const handleEnrich = async () => {
    setIsEnriching(true);
    const enriched = await onEnrichCoordinates(lat, lon);
    setIsEnriching(false);
    if (enriched) {
      if (enriched.climate_zone) setClimate(enriched.climate_zone);
      if (enriched.rainfall_annual_mm) setRainfall(enriched.rainfall_annual_mm);
      if (enriched.soil_organic_carbon_pct) setSoc(enriched.soil_organic_carbon_pct);
    }
  };

  const handleRun = () => {
    onDiagnose({
      coordinates: [lat, lon],
      soil_organic_carbon_pct: parseFloat(soc),
      soil_ph: parseFloat(ph),
      soil_bulk_density: parseFloat(bulkDensity),
      vegetative_ground_cover_pct: parseFloat(groundCover),
      rainfall_annual_mm: parseFloat(rainfall),
      climate_zone: climate,
      land_use_type: landUse,
      crop_type: crop,
      tillage_practice: tillage,
      pesticide_passes_yr: parseFloat(pesticides)
    });
  };

  const currentProfile = {
    soil_organic_carbon_pct: parseFloat(soc),
    soil_bulk_density: parseFloat(bulkDensity),
    vegetative_ground_cover_pct: parseFloat(groundCover),
    rainfall_annual_mm: parseFloat(rainfall),
    canopy_cover_pct: 5,
    pollinator_density_index: 25
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-12">
      {/* Studio Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Interactive Field Simulation
            </span>
            <span className="text-xs text-slate-400">Parameter Studio</span>
          </div>
          <h2 className="text-xl font-black text-white tracking-tight">
            Field Matrix &amp; Real-Time Radar Visualizer
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            {isLaymanMode 
              ? "Tweak your farm's soil, rainfall, and plowing to see live health scores and instant recommendations." 
              : "Calibrate multidimensional edaphic and bioclimatic parameters to observe non-linear causal degradation dynamics."}
          </p>
        </div>

        <button
          onClick={handleRun}
          className="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 shadow-lg shadow-emerald-950/50"
        >
          <Sparkles className="w-4 h-4" />
          <span>Synthesize Diagnosis &amp; Plan</span>
        </button>
      </div>

      {/* Main Studio Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Column: Parameter Controls (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          
          {/* Card 1: Location & Climate */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">1. Field Coordinates &amp; Climate</h3>
              </div>
              <button
                onClick={handleEnrich}
                disabled={isEnriching}
                className="text-xs text-emerald-300 hover:text-white bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-700/60 px-2.5 py-1 rounded-lg transition flex items-center gap-1.5"
              >
                <RefreshCw className={`w-3 h-3 ${isEnriching ? 'animate-spin' : ''}`} />
                <span>Auto-Detect Climate</span>
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">Latitude</label>
                <input 
                  type="number" 
                  step="0.1" 
                  value={lat} 
                  onChange={(e) => setLat(e.target.value)} 
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">Longitude</label>
                <input 
                  type="number" 
                  step="0.1" 
                  value={lon} 
                  onChange={(e) => setLon(e.target.value)} 
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
              <div>
                <div className="flex items-center justify-between text-[11px] mb-1">
                  <span className="font-semibold text-slate-300">Annual Rainfall: {rainfall} mm</span>
                  <span className={`px-1.5 py-0.2 rounded font-bold text-[10px] ${rainfall < 400 ? 'bg-amber-950 text-amber-300' : 'bg-slate-800 text-slate-300'}`}>
                    {rainfall < 400 ? 'Low (Dryland)' : 'Moderate'}
                  </span>
                </div>
                <input 
                  type="range" 
                  min="150" 
                  max="1200" 
                  step="10" 
                  value={rainfall} 
                  onChange={(e) => setRainfall(e.target.value)}
                  className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">Climate Zone</label>
                <select 
                  value={climate} 
                  onChange={(e) => setClimate(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="semi_arid">Semi-Arid (Dryland Basin)</option>
                  <option value="arid">Arid (Desert / High Drought)</option>
                  <option value="temperate">Temperate (Moderate)</option>
                  <option value="tropical">Tropical (Monsoonal)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Card 2: Soil Health Indicators */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">2. Soil Health &amp; Structure</h3>
              </div>
              <span className="text-[10px] text-slate-400">Key Drivers of Erosion</span>
            </div>

            {/* SOC Slider */}
            <div>
              <div className="flex items-center justify-between text-[11px] mb-1">
                <span className="font-semibold text-slate-200">
                  Soil Organic Carbon (SOC): <span className="font-mono text-emerald-400 font-bold">{soc}%</span>
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  soc <= 0.5 ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                  soc <= 1.5 ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                  'bg-emerald-950 text-emerald-300 border border-emerald-800'
                }`}>
                  {soc <= 0.5 ? '🔴 Critically Depleted' : soc <= 1.5 ? '🟡 Sub-Optimal' : '🟢 Healthy'}
                </span>
              </div>
              <input 
                type="range" 
                min="0.1" 
                max="4.0" 
                step="0.05" 
                value={soc} 
                onChange={(e) => setSoc(e.target.value)}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
              <p className="text-[10px] text-slate-400 mt-1">
                {isLaymanMode 
                  ? "Organic carbon is the glue and sponge of soil. Below 0.5%, soil particles fall apart and blow away as dust."
                  : "FAO Global Assessment: Levels below 0.5% indicate acute macroaggregate breakdown and glomalin starvation."}
              </p>
            </div>

            {/* Bulk Density Slider */}
            <div>
              <div className="flex items-center justify-between text-[11px] mb-1">
                <span className="font-semibold text-slate-200">
                  Bulk Density (Compaction): <span className="font-mono text-emerald-400 font-bold">{bulkDensity} g/cm³</span>
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  bulkDensity >= 1.5 ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                  bulkDensity >= 1.35 ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                  'bg-emerald-950 text-emerald-300 border border-emerald-800'
                }`}>
                  {bulkDensity >= 1.5 ? '🔴 Hard Packed' : bulkDensity >= 1.35 ? '🟡 Moderately Dense' : '🟢 Well Aerated'}
                </span>
              </div>
              <input 
                type="range" 
                min="0.9" 
                max="1.8" 
                step="0.02" 
                value={bulkDensity} 
                onChange={(e) => setBulkDensity(e.target.value)}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
              <p className="text-[10px] text-slate-400 mt-1">
                {isLaymanMode 
                  ? "High density means soil is crushed hard. Plant roots can't breathe or push through, and rain runs off."
                  : "Values >1.55 g/cm³ restrict root penetration and aerotropic microbial respiration."}
              </p>
            </div>

            {/* pH and Ground Cover */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
              <div>
                <div className="flex items-center justify-between text-[11px] mb-1">
                  <span className="font-semibold text-slate-300">Soil pH: {ph}</span>
                  <span className="text-[10px] text-slate-400">{ph < 6 ? 'Acidic' : ph > 7.5 ? 'Alkaline' : 'Neutral'}</span>
                </div>
                <input 
                  type="range" 
                  min="4.5" 
                  max="9.0" 
                  step="0.1" 
                  value={ph} 
                  onChange={(e) => setPh(e.target.value)}
                  className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                />
              </div>
              <div>
                <div className="flex items-center justify-between text-[11px] mb-1">
                  <span className="font-semibold text-slate-300">Living Ground Cover: {groundCover}%</span>
                  <span className={`text-[10px] font-bold ${groundCover < 30 ? 'text-rose-400' : 'text-emerald-400'}`}>
                    {groundCover < 30 ? 'High Erosion' : 'Protected'}
                  </span>
                </div>
                <input 
                  type="range" 
                  min="5" 
                  max="95" 
                  step="5" 
                  value={groundCover} 
                  onChange={(e) => setGroundCover(e.target.value)}
                  className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                />
              </div>
            </div>
          </div>

          {/* Card 3: Farm Management */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex items-center justify-between pb-2.5 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Sliders className="w-4 h-4 text-emerald-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">3. Farm Practices &amp; Inputs</h3>
              </div>
              <span className="text-[10px] text-slate-400">Disturbance Regimes</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">Crop &amp; Land Use</label>
                <select 
                  value={crop} 
                  onChange={(e) => setCrop(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="monoculture wheat">Monoculture Wheat (Continuous)</option>
                  <option value="monoculture cotton">Monoculture Cotton</option>
                  <option value="degraded_pasture">Degraded Pasture / Grazing</option>
                  <option value="polyculture_rotation">Rotational Polyculture (Diverse)</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 block mb-1">Tillage / Plowing</label>
                <select 
                  value={tillage} 
                  onChange={(e) => setTillage(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="conventional_deep">Conventional Deep Inversion Plowing</option>
                  <option value="reduced_till">Reduced / Chisel Tillage</option>
                  <option value="no_till_direct_seed">Zero-Till (Direct Seeding)</option>
                </select>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-[11px] mb-1">
                <span className="font-semibold text-slate-300">Pesticide Spray Passes: {pesticides} / year</span>
                <span className="text-[10px] text-slate-400">{pesticides >= 3 ? 'High Biocontrol Impact' : 'Low Impact'}</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="8" 
                step="0.5" 
                value={pesticides} 
                onChange={(e) => setPesticides(e.target.value)}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* Right Column: Live Visualizer & Simulation Radar (5 cols) */}
        <div className="lg:col-span-5 space-y-4 sticky top-20">
          {/* Radar Chart */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center justify-between">
              <span>Ecological Balance Radar</span>
              <span className="text-[10px] text-emerald-400 font-normal">Amber: Current | Emerald: Projected</span>
            </h3>
            <RadarChart 
              profile={currentProfile} 
              recommendations={activePlan?.recommendations || []} 
            />
          </div>

          {/* Quick Diagnosis Preview Card */}
          {activePlan && (
            <div className="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border border-amber-500/30 rounded-2xl p-5 shadow-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400">Current Diagnosis</span>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-amber-500/20 text-amber-400 border border-amber-500/30">
                  Risk: {(activePlan.diagnosis?.vulnerability_score || 69.8).toFixed(1)}/100
                </span>
              </div>
              <h4 className="text-sm font-bold text-white">
                {activePlan.diagnosis?.primary_degradation_pathway}
              </h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                {isLaymanMode 
                  ? "Your farm shows severe topsoil breakdown and moisture loss. Planting multi-species cover crops will restore organic matter and water infiltration."
                  : activePlan.diagnosis?.compound_risk_analysis}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
