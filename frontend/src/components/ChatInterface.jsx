import React, { useState } from 'react';
import { 
  Send, Sparkles, AlertCircle, CheckCircle, Bot, 
  User, ArrowRight, Sliders, FileText, Compass, ShieldAlert 
} from 'lucide-react';

export default function ChatInterface({
  messages,
  onSendMessage,
  isLoading,
  onSelectOption,
  onOpenStudio,
  onOpenReport,
  isLaymanMode
}) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[780px] bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
      {/* Chat Sub-Header */}
      <div className="px-6 py-3.5 border-b border-slate-800/80 bg-slate-950/70 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-white">Darukaa AI Land Advisor</h3>
            <p className="text-[11px] text-slate-400">
              {isLaymanMode 
                ? "Conversational Field Consultant • Simple Plain-English Advice" 
                : "Deterministic Causal Reasoning • Peer-Reviewed Evidence"}
            </p>
          </div>
        </div>

        <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20">
          Sufficiency Gate Active (≥ 3 Metrics)
        </span>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-4">
            <div className="w-14 h-14 rounded-2xl bg-emerald-950/60 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
              <Sparkles className="w-7 h-7" />
            </div>
            <div>
              <h4 className="text-base font-bold text-white">How can I help diagnose your land today?</h4>
              <p className="text-xs text-slate-400 max-w-md mt-1 leading-relaxed">
                Describe your field conditions naturally, or click a quick scenario below to test how our AI Environmental Scientist evaluates interacting ecological variables.
              </p>
            </div>

            {/* Starter Suggestion Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-2xl pt-2 text-left">
              <button
                onClick={() => onSendMessage("Soil organic carbon: 0.3%, Rainfall: low (320mm), Crop: monoculture wheat, Region: semi-arid")}
                className="bg-slate-950/80 hover:bg-emerald-950/50 border border-slate-800 hover:border-emerald-500/50 p-3.5 rounded-xl transition group flex flex-col justify-between"
              >
                <div>
                  <span className="text-emerald-400 text-xs font-bold block mb-1">🌾 Dryland Wheat</span>
                  <p className="text-[11px] text-slate-300">Semi-arid wheat field with severely depleted soil carbon (0.3%).</p>
                </div>
                <span className="text-[10px] text-emerald-400 mt-2 flex items-center gap-1 font-semibold group-hover:translate-x-0.5 transition">
                  Run diagnosis <ArrowRight className="w-3 h-3" />
                </span>
              </button>

              <button
                onClick={() => onSendMessage("Biodiversity is declining on my land")}
                className="bg-slate-950/80 hover:bg-amber-950/50 border border-slate-800 hover:border-amber-500/50 p-3.5 rounded-xl transition group flex flex-col justify-between"
              >
                <div>
                  <span className="text-amber-400 text-xs font-bold block mb-1">⚠️ Vague Health Query</span>
                  <p className="text-[11px] text-slate-300">"Biodiversity is declining" — triggers our targeted clarification gate.</p>
                </div>
                <span className="text-[10px] text-amber-400 mt-2 flex items-center gap-1 font-semibold group-hover:translate-x-0.5 transition">
                  Test clarification <ArrowRight className="w-3 h-3" />
                </span>
              </button>

              <button
                onClick={() => onSendMessage("Coordinates: (31.5, -102.3), SOC: 0.45%, BD: 1.52 g/cm³, Cotton Monoculture")}
                className="bg-slate-950/80 hover:bg-sky-950/50 border border-slate-800 hover:border-sky-500/50 p-3.5 rounded-xl transition group flex flex-col justify-between"
              >
                <div>
                  <span className="text-sky-400 text-xs font-bold block mb-1">📍 GPS Coordinates</span>
                  <p className="text-[11px] text-slate-300">High Plains basin coordinates with automatic climate lookup &amp; 0.4ms trace.</p>
                </div>
                <span className="text-[10px] text-sky-400 mt-2 flex items-center gap-1 font-semibold group-hover:translate-x-0.5 transition">
                  Run geo-trace <ArrowRight className="w-3 h-3" />
                </span>
              </button>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role !== 'user' && (
              <div className="w-8 h-8 rounded-xl bg-emerald-950 border border-emerald-700/60 text-emerald-400 flex items-center justify-center shrink-0 text-sm shadow-sm">
                🌱
              </div>
            )}

            <div
              className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-emerald-600 text-white font-medium rounded-tr-sm shadow-md'
                  : 'bg-slate-950/80 text-slate-200 border border-slate-800 rounded-tl-sm shadow-md'
              }`}
            >
              {/* Type 1: Clarification Message */}
              {msg.type === 'clarification' ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-amber-400 font-bold text-xs">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>More Data Needed (Sufficiency Gate Active)</span>
                  </div>

                  <p className="text-slate-200 font-medium leading-normal text-xs">
                    {msg.content}
                  </p>

                  {/* Missing Variables Badges */}
                  {msg.data?.clarification?.missing_critical_variables && (
                    <div className="space-y-1.5 pt-1">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">
                        Most Decision-Critical Missing Metrics:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.data.clarification.missing_critical_variables.map((v, vIdx) => (
                          <span
                            key={vIdx}
                            className="bg-amber-950/80 text-amber-300 border border-amber-800/60 px-2.5 py-0.5 rounded-md text-[11px] font-semibold"
                          >
                            • {v}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Quick Preset Buttons */}
                  {msg.data?.clarification?.suggested_quick_options && (
                    <div className="space-y-2 pt-2 border-t border-slate-800">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">
                        Or select a sample farm scenario to continue:
                      </span>
                      <div className="flex flex-col gap-1.5">
                        {msg.data.clarification.suggested_quick_options.map((opt, oIdx) => (
                          <button
                            key={oIdx}
                            onClick={() => onSelectOption(opt.text)}
                            className="text-left bg-slate-900 hover:bg-emerald-950/60 border border-slate-800 hover:border-emerald-500/50 p-2.5 rounded-xl transition group"
                          >
                            <div className="font-bold text-white group-hover:text-emerald-300 flex items-center justify-between text-xs">
                              <span>{opt.label}</span>
                              <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-emerald-400" />
                            </div>
                            <div className="text-[11px] text-slate-400 mt-0.5 font-mono truncate">
                              {opt.text}
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : msg.type === 'verified_plan' ? (
                /* Type 2: Verified Plan Message */
                <div className="space-y-3.5">
                  <div className="flex items-center justify-between gap-2 border-b border-slate-800 pb-2">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-emerald-400" />
                      <span className="font-bold text-white text-xs">Diagnosis &amp; Decision Plan Ready</span>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
                      Vulnerability: {(msg.data?.plan?.diagnosis?.vulnerability_score || 69.8).toFixed(1)}/100
                    </span>
                  </div>

                  <div>
                    <span className="text-[11px] font-bold text-amber-300 block mb-0.5">
                      {msg.data?.plan?.diagnosis?.primary_degradation_pathway || "Coupled Ecological Degradation"}
                    </span>
                    <p className="text-slate-300 text-[11px] leading-relaxed">
                      {msg.data?.plan?.diagnosis?.compound_risk_analysis || msg.content}
                    </p>
                  </div>

                  {/* 3 Prescriptions preview */}
                  <div className="space-y-1.5 pt-1">
                    <span className="text-[10px] uppercase font-bold text-slate-400 block">
                      Recommended Intervention Portfolio:
                    </span>
                    {(msg.data?.plan?.recommendations || []).map((r, rIdx) => (
                      <div key={rIdx} className="bg-slate-900 p-2 rounded-lg border border-slate-800 flex items-center justify-between">
                        <span className="font-semibold text-slate-200 text-xs">{rIdx + 1}. {r.title}</span>
                        <span className="text-[10px] text-emerald-400 font-mono">{r.time_horizon}</span>
                      </div>
                    ))}
                  </div>

                  {/* Quick Action Link to Studio and Report */}
                  <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800">
                    <button
                      onClick={onOpenStudio}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition"
                    >
                      <Sliders className="w-3.5 h-3.5" />
                      <span>Open Field Studio &amp; Radar Chart &rarr;</span>
                    </button>
                    <button
                      onClick={onOpenReport}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs transition border border-slate-700"
                    >
                      <FileText className="w-3.5 h-3.5" />
                      <span>Full Executive Report</span>
                    </button>
                  </div>
                </div>
              ) : (
                <div className="whitespace-pre-wrap">{msg.content}</div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-xl bg-slate-800 text-slate-300 flex items-center justify-center shrink-0 text-xs font-bold shadow-sm">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-emerald-950 border border-emerald-700/60 text-emerald-400 flex items-center justify-center shrink-0 text-sm animate-pulse">
              🌱
            </div>
            <div className="bg-slate-950 border border-slate-800 rounded-2xl px-4 py-2.5 text-xs text-slate-400 flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              Evaluating multi-variable diagnostic rules &amp; searching scientific literature...
            </div>
          </div>
        )}
      </div>

      {/* Input Field */}
      <form onSubmit={handleSubmit} className="p-4 bg-slate-950 border-t border-slate-800/80 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your soil, crop, rainfall or enter coordinates..."
          disabled={isLoading}
          className="flex-1 bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-1.5 transition shadow-md shadow-emerald-950/50"
        >
          <span>Send</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
