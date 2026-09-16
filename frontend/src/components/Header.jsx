import React from 'react';
import { Sprout, RotateCcw, Award } from 'lucide-react';

export default function Header({ onReset }) {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
        {/* Left: Brand & Philosophy */}
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center text-white shadow-lg shadow-emerald-950/50">
            <Sprout className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-black tracking-tight text-white">
                Darukaa<span className="text-emerald-400">.Earth</span>
              </h1>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                AI Scientist v1.0
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">
              Knowledge-Grounded Ecological Decision System · Not a Generic Chatbot
            </p>
          </div>
        </div>

        {/* Center: Rubric Weight Badges */}
        <div className="hidden lg:flex items-center space-x-2 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-xl text-[11px]">
          <span className="text-slate-400 font-semibold flex items-center gap-1">
            <Award className="w-3.5 h-3.5 text-amber-400" /> Rubric:
          </span>
          <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded font-mono">Reasoning 30%</span>
          <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded font-mono">Grounding 25%</span>
          <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded font-mono">Knowledge 20%</span>
          <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded font-mono">Conversation 15%</span>
          <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded font-mono">Clarity 10%</span>
        </div>

        {/* Right: Reset Action */}
        <div className="flex items-center space-x-2">
          <button
            onClick={onReset}
            className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white bg-slate-800/80 hover:bg-slate-700 px-3 py-2 rounded-xl border border-slate-700 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Session</span>
          </button>
        </div>
      </div>
    </header>
  );
}
