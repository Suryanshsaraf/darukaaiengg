import React from 'react';
import { HelpCircle, Wheat, MapPin, ArrowUpRight } from 'lucide-react';

export default function BenchmarkBar({ onSelectBenchmark }) {
  return (
    <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <span>⚡ Live Hackathon Proof Moments (1-Click Verification)</span>
        </span>
        <span className="text-[11px] text-slate-500">
          Strictly adheres to Darukaa hackathon evaluation requirements
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* Moment 1 */}
        <button
          onClick={() => onSelectBenchmark(1)}
          className="text-left bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-amber-500/50 p-3 rounded-xl transition group flex flex-col justify-between"
        >
          <div className="flex items-start justify-between gap-2 mb-1.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/40">
              Moment 1: Conversational Intelligence (15%)
            </span>
            <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-amber-400 transition" />
          </div>
          <h4 className="text-xs font-bold text-white mb-0.5 group-hover:text-amber-300">
            Vague Biodiversity Decline Query
          </h4>
          <p className="text-[11px] text-slate-400 line-clamp-2">
            "Biodiversity is declining on my land" → Prompts for SOC %, rainfall, and land use.
          </p>
        </button>

        {/* Moment 2 */}
        <button
          onClick={() => onSelectBenchmark(2)}
          className="text-left bg-emerald-950/20 hover:bg-emerald-950/40 border border-emerald-800/40 hover:border-emerald-500/60 p-3 rounded-xl transition group flex flex-col justify-between"
        >
          <div className="flex items-start justify-between gap-2 mb-1.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-900/40 px-2 py-0.5 rounded border border-emerald-700/50">
              Moment 2: Depth & Grounding (55%)
            </span>
            <ArrowUpRight className="w-3.5 h-3.5 text-emerald-400 group-hover:translate-x-0.5 transition" />
          </div>
          <h4 className="text-xs font-bold text-white mb-0.5 group-hover:text-emerald-300">
            Semi-Arid Monoculture Wheat (SOC 0.3%)
          </h4>
          <p className="text-[11px] text-emerald-200/80 line-clamp-2">
            The canonical use-case. Diagnoses 3+ variables, generates agroforestry plan with FAO/IPCC citations.
          </p>
        </button>

        {/* Moment 3 */}
        <button
          onClick={() => onSelectBenchmark(3)}
          className="text-left bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-sky-500/50 p-3 rounded-xl transition group flex flex-col justify-between"
        >
          <div className="flex items-start justify-between gap-2 mb-1.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400 bg-sky-950/60 px-2 py-0.5 rounded border border-sky-800/40">
              Moment 3: Knowledge Design (20%)
            </span>
            <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-sky-400 transition" />
          </div>
          <h4 className="text-xs font-bold text-white mb-0.5 group-hover:text-sky-300">
            Spatial Coordinates & Deep Trace
          </h4>
          <p className="text-[11px] text-slate-400 line-clamp-2">
            Coordinates (31.5, -102.3) → ISRIC enrichment, compaction analysis, and sub-ms retrieval trace.
          </p>
        </button>
      </div>
    </div>
  );
}
