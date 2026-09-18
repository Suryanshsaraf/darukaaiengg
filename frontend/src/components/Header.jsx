import React from 'react';
import { 
  Sprout, RotateCcw, Download, MessageSquare, 
  Sliders, FileText, Database, Sparkles, BookOpen, ChevronDown 
} from 'lucide-react';

export default function Header({ 
  activeTab, 
  onSelectTab, 
  isLaymanMode, 
  onToggleLaymanMode, 
  onSelectScenario,
  onReset,
  onDownloadJson
}) {
  return (
    <header className="border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md sticky top-0 z-50">
      <div className="w-full px-4 sm:px-6 lg:px-8 py-2.5 flex flex-wrap items-center justify-between gap-4">
        
        {/* Left: Branding */}
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center text-white shadow-md shadow-emerald-950/40">
            <Sprout className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-black tracking-tight text-white">
                Darukaa<span className="text-emerald-400">.Earth</span>
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                dMRV Engine
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">
              Autonomous Nature Intelligence &amp; Ecological Decision System
            </p>
          </div>
        </div>

        {/* Center: Main View Tabs */}
        <nav className="flex items-center bg-slate-900/90 p-1 rounded-xl border border-slate-800 text-xs font-semibold">
          <button
            onClick={() => onSelectTab('chat')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              activeTab === 'chat'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>AI Land Advisor</span>
          </button>

          <button
            onClick={() => onSelectTab('studio')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              activeTab === 'studio'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>Field Studio</span>
          </button>

          <button
            onClick={() => onSelectTab('report')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              activeTab === 'report'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Executive Plan</span>
          </button>

          <button
            onClick={() => onSelectTab('science')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              activeTab === 'science'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Database className="w-3.5 h-3.5" />
            <span>Audit &amp; Citations</span>
          </button>
        </nav>

        {/* Right: Controls & Layman Toggle */}
        <div className="flex items-center space-x-2.5">
          
          {/* Layman vs Scientific Toggle */}
          <button
            onClick={onToggleLaymanMode}
            className={`flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-xl border transition ${
              isLaymanMode
                ? 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60 shadow-sm'
                : 'bg-indigo-950/80 text-indigo-300 border-indigo-700/60 shadow-sm'
            }`}
            title="Toggle between simplified farmer language and deep scientific terminology"
          >
            <span>{isLaymanMode ? '🌱 Layman Mode' : '🔬 Deep Science'}</span>
          </button>

          {/* Quick Demo Scenarios Dropdown */}
          <div className="relative group">
            <button className="flex items-center gap-1.5 text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-300 px-3 py-1.5 rounded-xl border border-slate-700/80 transition">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>Demo Presets</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>

            <div className="absolute right-0 mt-1 w-56 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl py-1.5 hidden group-hover:block z-50">
              <button
                onClick={() => onSelectScenario(2)}
                className="w-full text-left px-3 py-2 text-xs text-slate-300 hover:bg-emerald-950/70 hover:text-white transition flex flex-col"
              >
                <span className="font-bold text-white">🌾 Semi-Arid Monoculture Wheat</span>
                <span className="text-[10px] text-slate-400">Canonical Dryland Degradation (SOC 0.3%)</span>
              </button>
              <button
                onClick={() => onSelectScenario(1)}
                className="w-full text-left px-3 py-2 text-xs text-slate-300 hover:bg-emerald-950/70 hover:text-white transition flex flex-col border-t border-slate-800/80"
              >
                <span className="font-bold text-white">⚠️ Vague Biodiversity Question</span>
                <span className="text-[10px] text-slate-400">Tests 3-variable clarification gate</span>
              </button>
              <button
                onClick={() => onSelectScenario(3)}
                className="w-full text-left px-3 py-2 text-xs text-slate-300 hover:bg-emerald-950/70 hover:text-white transition flex flex-col border-t border-slate-800/80"
              >
                <span className="font-bold text-white">📍 GPS Coordinates (High Plains)</span>
                <span className="text-[10px] text-slate-400">Triggers geo-lookup &amp; 0.4ms trace</span>
              </button>
            </div>
          </div>

          {/* Reset */}
          <button
            onClick={onReset}
            className="flex items-center space-x-1 text-xs text-slate-400 hover:text-white bg-slate-900 hover:bg-slate-800 px-2.5 py-1.5 rounded-xl border border-slate-800 transition"
            title="Reset active session"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </header>
  );
}
