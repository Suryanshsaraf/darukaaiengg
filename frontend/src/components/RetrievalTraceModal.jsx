import React from 'react';
import { X, ExternalLink, Cpu, CheckCircle2, Sliders, Database } from 'lucide-react';

export default function RetrievalTraceModal({ isOpen, onClose, trace }) {
  if (!isOpen || !trace) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                Deep Retrieval Trace Inspector
                <span className="text-[11px] font-semibold bg-emerald-500/15 text-emerald-400 px-2 py-0.5 rounded-full border border-emerald-500/30">
                  Sub-ms Latency
                </span>
              </h3>
              <p className="text-xs text-slate-400">
                Auditable BM25 lexical + TF-IDF vector cosine + metadata-filtered retrieval trace
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Trace Stats Header */}
        <div className="grid grid-cols-3 gap-3 p-6 pb-4 border-b border-slate-800 bg-slate-900/40">
          <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3">
            <span className="text-xs text-slate-400 block mb-1">Evaluated Candidate Chunks</span>
            <span className="text-lg font-bold text-white">{trace.candidate_chunks_evaluated || 16}</span>
          </div>
          <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3">
            <span className="text-xs text-slate-400 block mb-1">Passages Returned</span>
            <span className="text-lg font-bold text-emerald-400">{trace.chunks_returned_count || trace.top_chunks?.length || 0}</span>
          </div>
          <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3">
            <span className="text-xs text-slate-400 block mb-1">Retrieval Latency</span>
            <span className="text-lg font-bold text-sky-400">{(trace.execution_time_ms || 0.4).toFixed(2)} ms</span>
          </div>
        </div>

        {/* Filter & Query Section */}
        <div className="px-6 py-3 bg-slate-950/40 border-b border-slate-800 text-xs flex flex-wrap items-center gap-2">
          <span className="text-slate-400 font-semibold">Query String:</span>
          <code className="bg-slate-800 text-emerald-300 px-2 py-0.5 rounded border border-slate-700 text-[11px]">
            {trace.retrieval_query || "N/A"}
          </code>
          {trace.applied_filters && (
            <div className="flex items-center gap-1.5 ml-2">
              <span className="text-slate-400 font-semibold">Active Metadata Constraints:</span>
              <span className="bg-purple-950/60 text-purple-300 px-2 py-0.5 rounded border border-purple-800/50 text-[11px]">
                {JSON.stringify(trace.applied_filters)}
              </span>
            </div>
          )}
        </div>

        {/* Chunks List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {(trace.top_chunks || []).map((chunk, idx) => (
            <div
              key={idx}
              className="bg-slate-800/70 border border-slate-700/70 rounded-xl p-4 hover:border-emerald-500/50 transition shadow-sm"
            >
              <div className="flex items-start justify-between gap-4 mb-2">
                <div>
                  <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800/50 mr-2">
                    {chunk.chunk_id}
                  </span>
                  <h4 className="text-sm font-bold text-white inline">{chunk.source_title}</h4>
                  <div className="text-xs text-slate-400 mt-0.5">{chunk.authors_year}</div>
                </div>
                {chunk.doi_or_url && (
                  <a
                    href={chunk.doi_or_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300 font-medium shrink-0"
                  >
                    <span>Source DOI</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>

              {/* Score breakdown pills */}
              {chunk.scores && (
                <div className="flex flex-wrap items-center gap-2 my-2.5 text-[11px]">
                  <span className="bg-slate-900/80 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700 font-mono">
                    BM25: <b className="text-sky-400">{chunk.scores.bm25}</b>
                  </span>
                  <span className="bg-slate-900/80 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700 font-mono">
                    Vector Cosine: <b className="text-purple-400">{chunk.scores.vector_cosine}</b>
                  </span>
                  <span className="bg-slate-900/80 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700 font-mono">
                    Metadata Match: <b className="text-amber-400">{chunk.scores.metadata_bonus}</b>
                  </span>
                  <span className="bg-emerald-950/70 text-emerald-300 px-2.5 py-1 rounded-md border border-emerald-800/80 font-mono font-bold">
                    Composite Score: {chunk.scores.composite_relevance}
                  </span>
                </div>
              )}

              {/* Passage Excerpt */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-lg p-3 mt-2">
                <p className="text-xs text-slate-300 italic leading-relaxed">
                  "{chunk.excerpt}"
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between text-xs text-slate-500">
          <span>Darukaa.Earth Hybrid Retrieval Layer v1.0</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition"
          >
            Close Inspector
          </button>
        </div>
      </div>
    </div>
  );
}
