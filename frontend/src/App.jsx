import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import SiteMatrix from './components/SiteMatrix';
import PlanView from './components/PlanView';
import ScienceAuditView from './components/ScienceAuditView';
import RetrievalTraceModal from './components/RetrievalTraceModal';
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
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' | 'studio' | 'report' | 'science'
  const [isLaymanMode, setIsLaymanMode] = useState(true); // Default to Layman Friendly!
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substring(2, 9));

  // Initialize with Benchmark 2 on startup so data is immediately available across tabs
  useEffect(() => {
    handleSelectScenario(2, false);
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

  const applyScenarioData = (scenarioId, data, switchTab = true) => {
    if (scenarioId === 1) {
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
      if (switchTab) setActiveTab('chat');
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
      if (switchTab) {
        if (scenarioId === 3) setActiveTab('science');
        else setActiveTab('report');
      }
    }
  };

  const handleSelectScenario = async (scenarioId, switchTab = true) => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/benchmarks/${scenarioId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      applyScenarioData(scenarioId, data, switchTab);
    } catch (err) {
      console.warn("Backend benchmark unavailable, using client scenario:", err);
      const fallbackData = BENCHMARK_SCENARIOS[scenarioId] || BENCHMARK_SCENARIOS[2];
      applyScenarioData(scenarioId, fallbackData, switchTab);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setActivePlan(null);
    setRetrievalTrace(null);
    setSessionId('sess_' + Math.random().toString(36).substring(2, 9));
    setActiveTab('chat');
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
      {/* 1. Header with View Tabs & Layman Switch */}
      <Header 
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        isLaymanMode={isLaymanMode}
        onToggleLaymanMode={() => setIsLaymanMode(!isLaymanMode)}
        onSelectScenario={handleSelectScenario}
        onReset={handleReset}
        onDownloadJson={handleDownloadJson}
      />

      {/* 2. Main Tabbed Content Area */}
      <main className="flex-1 w-full px-4 sm:px-6 lg:px-8 py-5">
        {/* Tab 1: AI Land Advisor (Conversational Mode) */}
        {activeTab === 'chat' && (
          <ChatInterface 
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            onSelectOption={handleSendMessage}
            onOpenStudio={() => setActiveTab('studio')}
            onOpenReport={() => setActiveTab('report')}
            isLaymanMode={isLaymanMode}
          />
        )}

        {/* Tab 2: Field Studio (Interactive Simulation & Radar) */}
        {activeTab === 'studio' && (
          <SiteMatrix 
            onDiagnose={handleDiagnose}
            onEnrichCoordinates={handleEnrichCoordinates}
            activePlan={activePlan}
            isLaymanMode={isLaymanMode}
          />
        )}

        {/* Tab 3: Executive Plan (Structured Action Report) */}
        {activeTab === 'report' && (
          <PlanView 
            plan={activePlan}
            onOpenTrace={() => setActiveTab('science')}
            onDownloadJson={handleDownloadJson}
            isLaymanMode={isLaymanMode}
            onOpenStudio={() => setActiveTab('studio')}
          />
        )}

        {/* Tab 4: Science, Citations & Audit Trace (For Evaluators & Auditors) */}
        {activeTab === 'science' && (
          <ScienceAuditView 
            trace={retrievalTrace}
            plan={activePlan}
          />
        )}
      </main>

      {/* Deep Retrieval Trace Modal (Can also be opened directly) */}
      <RetrievalTraceModal 
        isOpen={isTraceOpen}
        onClose={() => setIsTraceOpen(false)}
        trace={retrievalTrace}
      />
    </div>
  );
}
