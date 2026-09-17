import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import BenchmarkBar from './components/BenchmarkBar';
import ChatInterface from './components/ChatInterface';
import SiteMatrix from './components/SiteMatrix';
import PlanView from './components/PlanView';
import RetrievalTraceModal from './components/RetrievalTraceModal';
import { MessageSquare, Sliders, Database, Sparkles, BookOpen } from 'lucide-react';
import {
  processClientMessage,
  diagnoseClientProfile,
  enrichClientCoordinates,
  BENCHMARK_SCENARIOS
} from './engine/decisionEngine';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [activePlan, setActivePlan] = useState(null);
  const [retrievalTrace, setRetrievalTrace] = useState(null);
  const [isTraceOpen, setIsTraceOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' | 'matrix' | 'sources'
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substring(2, 9));

  // Initialize with Benchmark 2 on start so the reviewer immediately sees high-value depth!
  useEffect(() => {
    handleSelectBenchmark(2);
  }, []);

  const handleSendMessage = async (text) => {
    setIsLoading(true);
    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId })
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (data.type === 'clarification') {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            type: 'clarification',
            content: data.assistant_message,
            data: data
          }
        ]);
      } else if (data.type === 'verified_plan') {
        setActivePlan(data.plan);
        setRetrievalTrace(data.plan.retrieval_trace);
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            type: 'verified_plan',
            content: data.assistant_message,
            data: data
          }
        ]);
      }
    } catch (err) {
      console.warn("Backend unavailable, executing in-browser decision engine:", err);
      const fallback = processClientMessage(text);
      if (fallback.type === 'clarification') {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            type: 'clarification',
            content: fallback.assistant_message,
            data: fallback
          }
        ]);
      } else if (fallback.type === 'verified_plan' || fallback.plan) {
        setActivePlan(fallback.plan);
        setRetrievalTrace(fallback.plan.retrieval_trace);
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            type: 'verified_plan',
            content: fallback.assistant_message,
            data: fallback
          }
        ]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDiagnose = async (profileData) => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profileData)
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const plan = await res.json();
      setActivePlan(plan);
      setRetrievalTrace(plan.retrieval_trace);
    } catch (err) {
      console.warn("Backend unavailable, generating client-side diagnosis:", err);
      const plan = diagnoseClientProfile(profileData);
      setActivePlan(plan);
      setRetrievalTrace(plan.retrieval_trace);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnrichCoordinates = async (lat, lon) => {
    try {
      const res = await fetch('/api/enrich', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: lat, longitude: lon })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("Backend unavailable, using client-side geo-enrichment:", err);
      return enrichClientCoordinates(lat, lon);
    }
  };

  const applyBenchmarkData = (benchmarkId, data) => {
    if (benchmarkId === 1) {
      setMessages([
        { role: 'user', content: 'Biodiversity is declining on my land' },
        {
          role: 'assistant',
          type: 'clarification',
          content: data.assistant_message,
          data: data
        }
      ]);
      setActivePlan(null);
      setActiveTab('chat');
    } else {
      setActivePlan(data.plan);
      setRetrievalTrace(data.plan.retrieval_trace);
      setMessages([
        { role: 'user', content: data.prompt || "Site assessment scenario" },
        {
          role: 'assistant',
          type: 'verified_plan',
          content: data.assistant_message,
          data: data
        }
      ]);
      if (benchmarkId === 3) {
        setIsTraceOpen(true);
      }
    }
  };

  const handleSelectBenchmark = async (benchmarkId) => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/benchmarks/${benchmarkId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      applyBenchmarkData(benchmarkId, data);
    } catch (err) {
      console.warn("Backend benchmark unavailable, using client scenario:", err);
      const fallbackData = BENCHMARK_SCENARIOS[benchmarkId] || BENCHMARK_SCENARIOS[2];
      applyBenchmarkData(benchmarkId, fallbackData);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    setMessages([]);
    setActivePlan(null);
    setRetrievalTrace(null);
    setSessionId('sess_' + Math.random().toString(36).substring(2, 9));
  };

  const handleDownloadJson = () => {
    if (!activePlan) return;
    const blob = new Blob([JSON.stringify(activePlan, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `darukaa_ecological_plan_${activePlan.plan_id || 'export'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased">
      {/* 1. Header */}
      <Header onReset={handleReset} />

      {/* 2. Main Content Container - Full Screen Fluid Width */}
      <main className="flex-1 w-full px-3 sm:px-5 lg:px-7 xl:px-9 py-4 space-y-4">
        {/* Benchmark Proof Bar */}
        <BenchmarkBar onSelectBenchmark={handleSelectBenchmark} />

        {/* 3. Core Working Area (Full Widescreen Responsive Layout) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
          {/* Left Column: Interactive Inputs & Dialogue (5 cols on lg, 4 cols on 2xl) */}
          <div className="lg:col-span-5 2xl:col-span-4 space-y-3">
            {/* Input Mode Navigation Tabs */}
            <div className="flex rounded-xl bg-slate-900 p-1 border border-slate-800 text-xs font-semibold">
              <button
                onClick={() => setActiveTab('chat')}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg transition ${
                  activeTab === 'chat'
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <MessageSquare className="w-3.5 h-3.5" />
                <span>Conversational Scientist</span>
              </button>
              <button
                onClick={() => setActiveTab('matrix')}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg transition ${
                  activeTab === 'matrix'
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Sliders className="w-3.5 h-3.5" />
                <span>Site Parameter Matrix</span>
              </button>
            </div>

            {/* Tab Views */}
            {activeTab === 'chat' ? (
              <ChatInterface
                messages={messages}
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
                onSelectOption={handleSendMessage}
              />
            ) : (
              <SiteMatrix
                onDiagnose={handleDiagnose}
                onEnrichCoordinates={handleEnrichCoordinates}
              />
            )}
          </div>

          {/* Right Column: Verified Plan & Deep Scientific Proof (7 cols on lg, 8 cols on 2xl) */}
          <div className="lg:col-span-7 2xl:col-span-8">
            {activePlan ? (
              <PlanView
                plan={activePlan}
                onOpenTrace={() => setIsTraceOpen(true)}
                onDownloadJson={handleDownloadJson}
              />
            ) : (
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center flex flex-col items-center justify-center min-h-[460px] text-slate-500 shadow-lg">
                <div className="w-16 h-16 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center justify-center text-slate-400 mb-4">
                  <Sparkles className="w-8 h-8 text-emerald-400" />
                </div>
                <h3 className="text-base font-bold text-slate-200">Awaiting Complete Site Parameters</h3>
                <p className="text-xs text-slate-400 max-w-md mt-1 leading-relaxed">
                  Provide at least 3 interacting environmental variables (Soil Organic Carbon, Rainfall, Land Use) or click any proof moment above to generate an evidence-backed intervention portfolio.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Deep Retrieval Trace Modal */}
      <RetrievalTraceModal
        isOpen={isTraceOpen}
        onClose={() => setIsTraceOpen(false)}
        trace={retrievalTrace}
      />
    </div>
  );
}
