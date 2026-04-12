const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChainEvent {
  type: string;
  chain: string;
  hash: string;
  from_address: string;
  to_address: string;
  token: string;
  amount: number;
  amount_usd: number;
  timestamp: string;
  analysis?: {
    importance: string;
    summary: string;
    insight: string;
  };
}

export interface NewsArticle {
  title: string;
  link: string;
  source: string;
  published_at: string;
}

export interface PriceData {
  symbol: string;
  name?: string;
  price: number;
  change_24h: number;
  market_cap?: number;
}

export async function fetchEvents(): Promise<ChainEvent[]> {
  const res = await fetch(`${API_BASE}/api/events`);
  const data = await res.json();
  return data.data || [];
}

export async function fetchNews(): Promise<NewsArticle[]> {
  const res = await fetch(`${API_BASE}/api/news`);
  const data = await res.json();
  return data.data || [];
}

export async function fetchPrices(): Promise<PriceData[]> {
  const res = await fetch(`${API_BASE}/api/prices`);
  const data = await res.json();
  return data.data || [];
}

export async function fetchLatestReport(): Promise<{ date: string; content: string }> {
  const res = await fetch(`${API_BASE}/api/report/latest`);
  return res.json();
}

export async function triggerRefresh() {
  await fetch(`${API_BASE}/api/refresh`);
}

export async function triggerReportGenerate() {
  const res = await fetch(`${API_BASE}/api/report/generate`, { method: "POST" });
  return res.json();
}
