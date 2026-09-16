import React, { useState } from 'react';
import { Send, Sparkles, AlertCircle, CheckCircle, Bot, User, ArrowRight } from 'lucide-react';

export default function ChatInterface({
  messages,
  onSendMessage,
  isLoading,
  onSelectOption
}) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl flex flex-col h-[740px] overflow-hidden shadow-xl">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Ecological Conversational Agent</h3>
            <p className="text-[11px] text-slate-400">Stateful context memory & targeted clarification gate</p>
          </div>
        </div>
        <span className="text-[11px] bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20 font-medium">
          Multi-Turn Memory Active
        </span>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500">
            <Bot className="w-12 h-12 text-slate-600 mb-3" />
            <h4 className="text-sm font-bold text-slate-300">Ready for Ecological Inquiry</h4>
            <p className="text-xs max-w-sm mt-1 text-slate-400 leading-relaxed">
              Submit a natural query like <span className="text-emerald-400 font-mono">"Biodiversity is declining on my land"</span> or provide specific metrics to trigger diagnosis.
            </p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role !== 'user' && (
              <div className="w-7 h-7 rounded-lg bg-emerald-600/30 text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-500/30 text-xs">
                🌱
              </div>
            )}

            <div
              className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-emerald-600 text-white font-medium rounded-tr-sm shadow-md'
                  : 'bg-slate-800/90 text-slate-200 border border-slate-700/80 rounded-tl-sm'
              }`}
            >
              {/* If it is a targeted clarification message */}
              {msg.type === 'clarification' ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-amber-400 font-bold">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>Targeted Clarification Required (Gate Enforced)</span>
                  </div>

                  <p className="text-slate-200 font-medium">{msg.content}</p>

                  {/* Missing Variables Badges */}
                  {msg.data?.clarification?.missing_critical_variables && (
                    <div className="space-y-1 pt-1">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">
                        Missing Decision-Critical Metrics:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.data.clarification.missing_critical_variables.map((v, vIdx) => (
                          <span
                            key={vIdx}
                            className="bg-amber-950/80 text-amber-300 border border-amber-800/60 px-2 py-0.5 rounded text-[11px] font-semibold"
                          >
                            • {v}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Quick Benchmark Preset Options */}
                  {msg.data?.clarification?.suggested_quick_options && (
                    <div className="space-y-1.5 pt-2 border-t border-slate-700/60">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">
                        Or select a standard benchmark scenario:
                      </span>
                      <div className="flex flex-col gap-1.5">
                        {msg.data.clarification.suggested_quick_options.map((opt, oIdx) => (
                          <button
                            key={oIdx}
                            onClick={() => onSelectOption(opt.text)}
                            className="text-left bg-slate-900/90 hover:bg-emerald-950/60 border border-slate-700/60 hover:border-emerald-500/50 p-2.5 rounded-lg transition group"
                          >
                            <div className="font-semibold text-white group-hover:text-emerald-300 flex items-center justify-between">
                              <span>{opt.label}</span>
                              <ArrowRight className="w-3 h-3 text-slate-400 group-hover:text-emerald-400" />
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
              ) : (
                <div className="whitespace-pre-wrap">{msg.content}</div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-7 h-7 rounded-lg bg-slate-700 text-slate-300 flex items-center justify-center shrink-0 text-xs">
                <User className="w-3.5 h-3.5" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-emerald-600/30 text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-500/30 text-xs animate-pulse">
              🌱
            </div>
            <div className="bg-slate-800/80 border border-slate-700 rounded-2xl px-4 py-2.5 text-xs text-slate-400 flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              Evaluating multi-variable causal matrix & retrieving scientific citations...
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-4 bg-slate-950/70 border-t border-slate-800 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type site conditions or answer clarifying questions..."
          disabled={isLoading}
          className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2.5 rounded-xl font-semibold text-xs flex items-center gap-1.5 transition shadow-md"
        >
          <span>Send</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
