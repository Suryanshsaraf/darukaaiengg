import React, { useState } from 'react';
import { Sliders, MapPin, Sparkles, RefreshCw, Layers } from 'lucide-react';

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

  const handleEnrich = async () => {
    const enriched = await onEnrichCoordinates(lat, lon);
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
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Sliders className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Manual Site Parameter Matrix</h3>
            <p className="text-[11px] text-slate-400">Direct parameter synthesis across all 5 ecological dimensions</p>
          </div>
        </div>

        <button
          onClick={handleRun}
          className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-md shadow-emerald-950/40"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Synthesize Diagnosis</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Col 1: Spatial & Climate Coordinates */}
        <div className="space-y-4 bg-slate-950/50 p-4 rounded-xl border border-slate-800/80">
          <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5" />
            1. Spatial Coordinates & Climate
          </span>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Latitude</label>
              <input
                type="number"
                step="0.001"
                value={lat}
                onChange={(e) => setLat(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
              />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Longitude</label>
              <input
                type="number"
                step="0.001"
                value={lon}
                onChange={(e) => setLon(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
              />
            </div>
          </div>

          <button
            onClick={handleEnrich}
            className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs py-2 rounded-lg font-medium transition border border-slate-700 flex items-center justify-center gap-1.5"
          >
            <RefreshCw className="w-3 h-3 text-emerald-400" />
            <span>Enrich from Geo-Coordinates</span>
          </button>

          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Mean Annual Precipitation (mm)</label>
            <input
              type="number"
              value={rainfall}
              onChange={(e) => setRainfall(parseFloat(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white font-mono"
            />
          </div>

          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Bioclimatic Zone</label>
            <select
              value={climate}
              onChange={(e) => setClimate(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
            >
              <option value="semi_arid">Semi-Arid (P/PET 0.20-0.50)</option>
              <option value="arid">Arid (P/PET 0.05-0.20)</option>
              <option value="dry_sub_humid">Dry Sub-Humid</option>
              <option value="temperate">Temperate Oceanic / Continental</option>
              <option value="tropical">Tropical Wet/Dry</option>
            </select>
          </div>
        </div>

        {/* Col 2: Pedological Health */}
        <div className="space-y-4 bg-slate-950/50 p-4 rounded-xl border border-slate-800/80">
          <span className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5" />
            2. Soil & Pedological State
          </span>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-400">Soil Organic Carbon (SOC %):</span>
              <span className={`font-mono font-bold ${soc < 0.5 ? 'text-red-400' : soc < 1.5 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {soc.toFixed(2)}% {soc < 0.5 ? '(Acute Desertification)' : ''}
              </span>
            </div>
            <input
              type="range"
              min="0.1"
              max="5.0"
              step="0.05"
              value={soc}
              onChange={(e) => setSoc(parseFloat(e.target.value))}
              className="w-full accent-emerald-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-400">Soil pH:</span>
              <span className="font-mono font-bold text-slate-200">{ph.toFixed(1)}</span>
            </div>
            <input
              type="range"
              min="4.0"
              max="9.5"
              step="0.1"
              value={ph}
              onChange={(e) => setPh(parseFloat(e.target.value))}
              className="w-full accent-emerald-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-400">Bulk Density (g/cm³):</span>
              <span className={`font-mono font-bold ${bulkDensity > 1.50 ? 'text-rose-400' : 'text-slate-200'}`}>
                {bulkDensity.toFixed(2)} g/cm³ {bulkDensity > 1.50 ? '(Compacted)' : ''}
              </span>
            </div>
            <input
              type="range"
              min="0.9"
              max="1.9"
              step="0.02"
              value={bulkDensity}
              onChange={(e) => setBulkDensity(parseFloat(e.target.value))}
              className="w-full accent-emerald-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-400">Vegetative Ground Cover %:</span>
              <span className="font-mono font-bold text-slate-200">{groundCover}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={groundCover}
              onChange={(e) => setGroundCover(parseInt(e.target.value))}
              className="w-full accent-emerald-500"
            />
          </div>
        </div>

        {/* Col 3: Land Use & Disturbance */}
        <div className="space-y-4 bg-slate-950/50 p-4 rounded-xl border border-slate-800/80">
          <span className="text-xs font-bold text-sky-400 uppercase tracking-wider flex items-center gap-1.5">
            🚜 3. Land Use & Disturbance
          </span>

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
            <label className="text-[11px] text-slate-400 block mb-1">Dominant Crop / Vegetation</label>
            <input
              type="text"
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
            />
          </div>

          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Tillage Management</label>
            <select
              value={tillage}
              onChange={(e) => setTillage(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white"
            >
              <option value="conventional_deep">Conventional Deep Inversion Plowing</option>
              <option value="reduced_till">Reduced / Strip Tillage</option>
              <option value="no_till_direct_seed">Zero-Tillage (Direct Seeding)</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Pesticide Passes / Year</label>
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
  );
}
