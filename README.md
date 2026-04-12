# 🔭 Web3Scope

**AI-Powered On-Chain Monitoring Platform**

Web3Scope is a full-stack platform that monitors blockchain transactions, aggregates Web3 news, and uses AI to generate intelligent daily reports with real-time alerts.

## ✨ Features

- **⛓️ On-Chain Monitoring** — Track large ETH transfers (>100K USD) in real-time via Alchemy
- **📰 News Aggregation** — Aggregates news from The Block, CoinDesk, Cointelegraph, PANews, and BlockBeats
- **📈 Market Data** — Real-time token prices from Binance API
- **🤖 AI Analysis** — Powered by LLM to analyze on-chain events and generate daily reports
- **📊 Daily Reports** — Auto-generated Web3 daily briefing pushed to Discord
- **🚨 Smart Alerts** — AI-classified event importance (🔴 High / 🟡 Medium / 🟢 Low)
- **🌐 Web Dashboard** — Clean, real-time dashboard built with Next.js

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend   │────▶│   Backend   │────▶│  AI Agent   │
│  Next.js +   │ API │  FastAPI +  │     │  GLM-4.5    │
│  Tailwind    │◀────│  Python     │────▶│             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌─────────┐ ┌─────────┐ ┌──────────┐
         │ Alchemy │ │ Binance │ │  RSS +   │
         │  (ETH)  │ │ (Price) │ │ Web Scrap│
         └─────────┘ └─────────┘ └──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Discord   │
                    │  Webhook    │
                    └─────────────┘
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn |
| AI | GLM-4.5 (OpenAI-compatible API) |
| Blockchain | Alchemy API (Ethereum) |
| Market Data | Binance Public API |
| News | RSS + BeautifulSoup Web Scraping |
| Push | Discord Webhook |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Alchemy API Key ([Get one free](https://www.alchemy.com))
- LLM API Key (DeepSeek / GLM / OpenAI)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events` | Latest on-chain events |
| GET | `/api/news` | Latest Web3 news |
| GET | `/api/prices` | Token market data |
| GET | `/api/report/latest` | Latest daily report |
| GET | `/api/reports` | List all reports |
| POST | `/api/report/generate` | Generate & push new report |
| POST | `/api/refresh` | Refresh all data |

## 📁 Project Structure

```
web3scope/
├── backend/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Configuration
│   ├── fetcher/
│   │   ├── chain.py         # On-chain data (Alchemy)
│   │   └── news.py          # News aggregation
│   ├── analyzer/
│   │   └── agent.py         # AI analysis & report gen
│   ├── pusher/
│   │   └── discord.py       # Discord webhook push
│   └── models/
│       └── schemas.py       # Data models
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx     # Dashboard
│       │   └── layout.tsx
│       ├── components/
│       │   ├── PriceCard.tsx
│       │   ├── EventRow.tsx
│       │   └── NewsItem.tsx
│       └── lib/
│           └── api.ts       # API client
└── reports/                 # Daily report archives
```

## 🗺️ Roadmap

- [x] Phase 1: Core monitoring & daily reports
- [ ] Phase 2: User subscriptions & custom alerts
- [ ] Phase 3: Multi-chain support (BSC, Solana)
- [ ] Phase 4: Natural language query interface
- [ ] Phase 5: Deploy to production (Vercel + Railway)

## 📄 License

MIT
