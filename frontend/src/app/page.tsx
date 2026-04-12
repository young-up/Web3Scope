"use client";

import { useEffect, useState } from "react";
import { fetchEvents, fetchNews, fetchPrices, fetchLatestReport, triggerRefresh, triggerReportGenerate } from "@/lib/api";
import { ChainEvent, NewsArticle, PriceData } from "@/lib/api";
import { PriceCard } from "@/components/PriceCard";
import { EventRow } from "@/components/EventRow";
import { NewsItem } from "@/components/NewsItem";

export default function Home() {
  const [events, setEvents] = useState<ChainEvent[]>([]);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [prices, setPrices] = useState<PriceData[]>([]);
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [tab, setTab] = useState<"overview" | "events" | "news" | "report">("overview");

  const loadData = async () => {
    setLoading(true);
    const [e, n, p, r] = await Promise.all([
      fetchEvents(),
      fetchNews(),
      fetchPrices(),
      fetchLatestReport(),
    ]);
    setEvents(e);
    setNews(n);
    setPrices(p);
    setReport(r.content || "");
    setLoading(false);
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 300000); // 5分钟刷新
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = async () => {
    await triggerRefresh();
    await loadData();
  };

  const handleGenerateReport = async () => {
    setGenerating(true);
    await triggerReportGenerate();
    const r = await fetchLatestReport();
    setReport(r.content || "");
    setGenerating(false);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Header */}
      <header className="border-b border-white/10 bg-[#0a0a0f]/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              🔭 Web3Scope
            </h1>
            <span className="text-xs text-gray-500">链上智能监控平台</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleRefresh}
              className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-sm hover:bg-white/10 transition-all"
            >
              🔄 刷新数据
            </button>
            <button
              onClick={handleGenerateReport}
              disabled={generating}
              className="px-3 py-1.5 rounded-lg bg-blue-600 text-sm hover:bg-blue-700 transition-all disabled:opacity-50"
            >
              {generating ? "⏳ 生成中..." : "📊 生成日报"}
            </button>
          </div>
        </div>
        {/* Tabs */}
        <div className="max-w-7xl mx-auto px-6 flex gap-1">
          {(["overview", "events", "news", "report"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm border-b-2 transition-all ${
                tab === t
                  ? "border-blue-400 text-blue-400"
                  : "border-transparent text-gray-400 hover:text-white"
              }`}
            >
              {t === "overview" ? "📋 总览" : t === "events" ? "⛓️ 链上事件" : t === "news" ? "📰 新闻" : "📄 日报"}
            </button>
          ))}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-400">加载中...</div>
        ) : tab === "overview" ? (
          <Overview events={events} news={news} prices={prices} report={report} onGenerate={handleGenerateReport} generating={generating} />
        ) : tab === "events" ? (
          <div className="space-y-3">
            <h2 className="text-lg font-semibold mb-4">⛓️ 链上大额事件 ({events.length})</h2>
            {events.length === 0 ? (
              <div className="text-gray-500 text-center py-12">
                暂无数据。请配置 Alchemy API Key 以启用链上监控。
              </div>
            ) : (
              events.map((e, i) => <EventRow key={i} event={e} />)
            )}
          </div>
        ) : tab === "news" ? (
          <div className="space-y-3">
            <h2 className="text-lg font-semibold mb-4">📰 Web3 新闻 ({news.length})</h2>
            {news.map((n, i) => <NewsItem key={i} article={n} />)}
          </div>
        ) : (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">📄 今日日报</h2>
              <button
                onClick={handleGenerateReport}
                disabled={generating}
                className="px-3 py-1.5 rounded-lg bg-blue-600 text-sm hover:bg-blue-700 disabled:opacity-50"
              >
                {generating ? "⏳ 生成中..." : "📊 重新生成"}
              </button>
            </div>
            <div className="bg-white/5 rounded-xl p-6 border border-white/10 prose prose-invert max-w-none">
              <pre className="whitespace-pre-wrap font-sans text-gray-200 text-sm leading-relaxed">{report || "暂无日报，点击上方按钮生成"}</pre>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function Overview({ events, news, prices, report, onGenerate, generating }: {
  events: ChainEvent[]; news: NewsArticle[]; prices: PriceData[];
  report: string; onGenerate: () => void; generating: boolean;
}) {
  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white/5 rounded-xl p-4 border border-white/10">
          <p className="text-gray-400 text-sm">链上事件</p>
          <p className="text-2xl font-bold mt-1">{events.length}</p>
        </div>
        <div className="bg-white/5 rounded-xl p-4 border border-white/10">
          <p className="text-gray-400 text-sm">新闻抓取</p>
          <p className="text-2xl font-bold mt-1">{news.length}</p>
        </div>
        <div className="bg-white/5 rounded-xl p-4 border border-white/10">
          <p className="text-gray-400 text-sm">监控代币</p>
          <p className="text-2xl font-bold mt-1">{prices.length}</p>
        </div>
        <div className="bg-white/5 rounded-xl p-4 border border-white/10">
          <p className="text-gray-400 text-sm">ETH价格</p>
          <p className="text-2xl font-bold mt-1">
            ${prices.find(p => p.symbol === "ETH")?.price.toLocaleString() || "—"}
          </p>
        </div>
      </div>

      {/* Prices */}
      <div>
        <h2 className="text-lg font-semibold mb-3">📈 市场行情</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {prices.map((p, i) => <PriceCard key={i} data={p} />)}
        </div>
      </div>

      {/* Recent events + news side by side */}
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold mb-3">⛓️ 最新链上事件</h2>
          <div className="space-y-2">
            {events.length === 0 ? (
              <p className="text-gray-500 text-sm">暂无数据，请配置Alchemy API Key</p>
            ) : (
              events.slice(0, 5).map((e, i) => <EventRow key={i} event={e} />)
            )}
          </div>
        </div>
        <div>
          <h2 className="text-lg font-semibold mb-3">📰 最新新闻</h2>
          <div className="space-y-2">
            {news.slice(0, 5).map((n, i) => <NewsItem key={i} article={n} />)}
          </div>
        </div>
      </div>

      {/* Report preview */}
      {report && (
        <div>
          <h2 className="text-lg font-semibold mb-3">📄 最新日报</h2>
          <div className="bg-white/5 rounded-xl p-5 border border-white/10">
            <pre className="whitespace-pre-wrap font-sans text-gray-200 text-sm leading-relaxed max-h-80 overflow-y-auto">
              {report.slice(0, 800)}...
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
