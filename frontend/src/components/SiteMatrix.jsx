import React, { useState } from 'react';
import { Sliders, MapPin, Sparkles, RefreshCw, Layers, ShieldAlert, Cpu } from 'lucide-react';

export default function SiteMatrix({ onDiagnose, onEnrichCoordinates }) {
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

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Sliders className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Manual Site Parameter Matrix</h3>
            <p className="text-[11px] text-slate-400">Parameter synthesis across all 5 ecological dimensions</p>
          </div>
        </div>

        <button
          onClick={handleRun}
          className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-md shadow-emerald-950/40 shrink-0"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Synthesize Diagnosis</span>
        </button>
      </div>

      {/* Spacious Sections */}
      <div className="space-y-4 max-h-[640px] overflow-y-auto pr-1">
        {/* Section 1: Location & Climate */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5" />
              1. Spatial Context & Climate
            </span>
            <button
              onClick={handleEnrich}
              disabled={isEnriching}
              className="bg-slate-800 hover:bg-slate-700 text-emerald-400 text-[11px] px-2.5 py-1 rounded-md transition border border-slate-700 flex items-center gap-1 font-semibold"
            >
              <RefreshCw className={`w-3 h-3 ${isEnriching ? 'animate-spin' : ''}`} />
              <span>Auto-Enrich ISRIC Baselines</span>
            </button>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Latitude</label>
              <input
                type="number"
                step="0.001"
                value={lat}
                onChange={(e) => setLat(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Longitude</label>
              <input
                type="number"
                step="0.001"
                value={lon}
                onChange={(e) => setLon(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Precipitation (mm/yr)</label>
              <input
                type="number"
                value={rainfall}
                onChange={(e) => setRainfall(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Climate Classification</label>
              <select
                value={climate}
                onChange={(e) => setClimate(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white"
              >
                <option value="semi_arid">Semi-Arid (P/PET 0.20-0.50)</option>
                <option value="arid">Arid (P/PET 0.05-0.20)</option>
                <option value="dry_sub_humid">Dry Sub-Humid</option>
                <option value="temperate">Temperate Oceanic / Continental</option>
                <option value="tropical">Tropical Wet/Dry</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Soil & Pedological Health */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3.5">
          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5" />
            2. Soil & Pedological State
          </span>

          {/* SOC Slider */}
          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-300 font-medium">Soil Organic Carbon (SOC %):</span>
              <span className={`font-mono font-bold px-2 py-0.5 rounded text-[11px] ${
                soc < 0.5 ? 'bg-rose-950 text-rose-300 border border-rose-800' : 
                soc < 1.5 ? 'bg-amber-950 text-amber-300 border border-amber-800' : 
                'bg-emerald-950 text-emerald-300 border border-emerald-800'
              }`}>
                {soc.toFixed(2)}% {soc < 0.5 ? '· Acute Desertification' : soc < 1.5 ? '· Depleted' : '· Healthy'}
              </span>
            </div>
            <input
              type="range"
              min="0.1"
              max="5.0"
              step="0.05"
              value={soc}
              onChange={(e) => setSoc(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
            />
          </div>

          {/* Bulk Density & pH */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-300">Soil pH:</span>
                <span className="font-mono font-bold text-slate-200">{ph.toFixed(1)}</span>
              </div>
              <input
                type="range"
                min="4.0"
                max="9.5"
                step="0.1"
                value={ph}
                onChange={(e) => setPh(parseFloat(e.target.value))}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
            </div>

            <div className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-300">Bulk Density:</span>
                <span className={`font-mono font-bold text-[11px] ${bulkDensity > 1.50 ? 'text-rose-400' : 'text-slate-200'}`}>
                  {bulkDensity.toFixed(2)} g/cm³
                </span>
              </div>
              <input
                type="range"
                min="0.9"
                max="1.9"
                step="0.02"
                value={bulkDensity}
                onChange={(e) => setBulkDensity(parseFloat(e.target.value))}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
            </div>
          </div>

          {/* Ground Cover */}
          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-300">Vegetative Ground Cover %:</span>
              <span className="font-mono font-bold text-slate-200">{groundCover}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={groundCover}
              onChange={(e) => setGroundCover(parseInt(e.target.value))}
              className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
            />
          </div>
        </div>

        {/* Section 3: Land Use & Agrochemical Disturbances */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
          <span className="text-xs font-bold text-sky-400 uppercase tracking-wider flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5" />
            3. Land Use & Disturbance Regime
          </span>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Land Use Regime</label>
              <select
                value={landUse}
                onChange={(e) => setLandUse(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
              >
                <option value="monoculture_cropland">Monoculture Cropland</option>
                <option value="intensive_tillage_cropland">Intensive Tillage Cropland</option>
                <option value="degraded_pasture">Degraded Continuous Pasture</option>
                <option value="rotational_pasture">Rotational Pasture</option>
              </select>
            </div>

            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Crop / Forage Type</label>
              <input
                type="text"
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Tillage Management</label>
              <select
                value={tillage}
                onChange={(e) => setTillage(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
              >
                <option value="conventional_deep">Conventional Deep Plowing</option>
                <option value="reduced_till">Reduced / Strip Tillage</option>
                <option value="no_till_direct_seed">Zero-Tillage (Direct Seeding)</option>
              </select>
            </div>

            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Pesticide Spray Passes / Year</label>
              <input
                type="number"
                min="0"
                max="15"
                step="0.5"
                value={pesticides}
                onChange={(e) => setPesticides(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white font-mono"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
