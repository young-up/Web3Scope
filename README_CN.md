[English](./README.md) | **中文**

# 🔭 Web3Scope

**AI 驱动的链上智能监控平台**

Web3Scope 是一个全栈平台，实时监控区块链大额交易、聚合 Web3 新闻资讯，并通过 AI 智能分析生成每日日报，支持实时告警推送。

## ✨ 功能特性

- **⛓️ 链上监控** — 通过 Alchemy 实时追踪 ETH 大额转账（>10万美元）
- **📰 新闻聚合** — 聚合 The Block、CoinDesk、Cointelegraph、PANews、BlockBeats 等 Web3 媒体新闻
- **📈 行情数据** — 通过 Binance API 获取实时代币价格
- **🤖 AI 分析** — 基于 LLM 智能分析链上事件，自动生成每日研报
- **📊 日报推送** — 自动生成 Web3 日报并推送至 Discord
- **🚨 智能分级** — AI 自动标注事件重要程度（🔴 重要 / 🟡 值得关注 / 🟢 一般）
- **🌐 Web 看板** — 基于 Next.js 构建的实时数据大盘

## 🏗️ 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    前端      │────▶│    后端      │────▶│  AI Agent   │
│  Next.js +  │ API │  FastAPI +  │     │   GLM-4.5   │
│  Tailwind   │◀────│   Python    │────▶│             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌─────────┐ ┌─────────┐ ┌──────────┐
         │ Alchemy │ │ Binance │ │  RSS +   │
         │  (ETH)  │ │ (行情)  │ │ 网页爬虫 │
         └─────────┘ └─────────┘ └──────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Discord   │
                    │  Webhook    │
                    └─────────────┘
```

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Next.js 16, TypeScript, Tailwind CSS |
| 后端 | Python, FastAPI, Uvicorn |
| AI | GLM-4.5（兼容 OpenAI 接口） |
| 区块链 | Alchemy API（以太坊） |
| 行情数据 | Binance 公开 API |
| 新闻采集 | RSS + BeautifulSoup 网页爬虫 |
| 推送 | Discord Webhook |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- Alchemy API Key（[免费注册](https://www.alchemy.com)）
- LLM API Key（DeepSeek / 智谱GLM / OpenAI）

### 后端启动

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入你的 API Key
python main.py
```

后端运行在 `http://localhost:8000`

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:3000`

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/events` | 最新链上事件 |
| GET | `/api/news` | 最新 Web3 新闻 |
| GET | `/api/prices` | 代币行情数据 |
| GET | `/api/report/latest` | 最新日报 |
| GET | `/api/reports` | 历史日报列表 |
| POST | `/api/report/generate` | 生成并推送日报 |
| POST | `/api/refresh` | 刷新所有数据 |

## 📁 项目结构

```
web3scope/
├── backend/
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置文件
│   ├── fetcher/
│   │   ├── chain.py         # 链上数据采集（Alchemy）
│   │   └── news.py          # 新闻聚合
│   ├── analyzer/
│   │   └── agent.py         # AI 分析 & 日报生成
│   ├── pusher/
│   │   └── discord.py       # Discord 推送
│   └── models/
│       └── schemas.py       # 数据模型
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx     # 数据大盘
│       │   └── layout.tsx   # 布局
│       ├── components/
│       │   ├── PriceCard.tsx  # 价格卡片
│       │   ├── EventRow.tsx   # 事件行
│       │   └── NewsItem.tsx   # 新闻条目
│       └── lib/
│           └── api.ts       # API 客户端
└── reports/                 # 日报存档
```

## 🗺️ 路线图

- [x] Phase 1：核心监控 & 每日日报
- [ ] Phase 2：用户订阅 & 自定义告警
- [ ] Phase 3：多链支持（BSC、Solana）
- [ ] Phase 4：自然语言查询接口
- [ ] Phase 5：生产环境部署（Vercel + Railway）

## 📄 许可证

MIT
