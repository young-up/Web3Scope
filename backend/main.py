import os
import json
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from fetcher.chain import fetch_latest_transfers, fetch_top_tokens
from fetcher.news import fetch_all_news
from analyzer.agent import analyze_events, generate_daily_report
from pusher.discord import push_discord_embed

app = FastAPI(title="Web3Scope", description="链上智能监控平台API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_executor = ThreadPoolExecutor(max_workers=4)

# 内存缓存
_cache = {
    "events": [],
    "news": [],
    "prices": [],
    "reports": [],
    "last_update": None,
}

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


@app.get("/api/events")
async def get_events():
    """获取最新链上事件"""
    return {"data": _cache["events"], "count": len(_cache["events"])}


@app.get("/api/news")
async def get_news():
    """获取最新新闻"""
    return {"data": _cache["news"], "count": len(_cache["news"])}


@app.get("/api/prices")
async def get_prices():
    """获取行情数据"""
    return {"data": _cache["prices"]}


@app.get("/api/report/latest")
async def get_latest_report():
    """获取最新日报"""
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"{today}.md"
    if report_path.exists():
        return {"date": today, "content": report_path.read_text(encoding="utf-8")}
    return {"date": today, "content": "今日报告尚未生成"}


@app.get("/api/reports")
async def list_reports():
    """列出所有日报"""
    reports = sorted(REPORTS_DIR.glob("*.md"), reverse=True)
    return {"data": [{"date": f.stem, "url": f"/api/report/{f.stem}"} for f in reports]}


@app.get("/api/refresh")
async def refresh_data():
    """手动刷新数据"""
    await update_all()
    return {"status": "ok", "events": len(_cache["events"]), "news": len(_cache["news"])}


@app.post("/api/report/generate")
async def generate_report(push: bool = True):
    """生成并推送日报"""
    title = f"Web3Scope日报 | {datetime.now().strftime('%m月%d日')}"
    report = generate_daily_report(_cache["events"], _cache["news"], _cache["prices"])
    if report and push:
        push_discord_embed(title, report)
    # 保存
    report_path = REPORTS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    report_path.write_text(f"## {title}\n\n{report}", encoding="utf-8")
    return {"status": "ok", "length": len(report)}


def _update_all_sync():
    """同步更新数据（在线程中运行）"""
    print(f"\n[{datetime.now().strftime('%H:%M')}] 刷新数据...")
    
    _cache["news"] = fetch_all_news()
    _cache["last_update"] = datetime.now().isoformat()

    try:
        prices = fetch_top_tokens()
        _cache["prices"] = prices
    except Exception as e:
        print(f"[刷新] 行情获取跳过: {e}")

    try:
        _cache["events"] = fetch_latest_transfers(20)
        if _cache["events"]:
            analyses = analyze_events(_cache["events"])
            for a in analyses:
                for e in _cache["events"]:
                    if a.get("hash") == e.get("hash"):
                        e["analysis"] = a
    except Exception as e:
        print(f"[刷新] 链上数据跳过: {e}")

    print(f"[刷新] 事件:{len(_cache['events'])} 新闻:{len(_cache['news'])} 价格:{len(_cache['prices'])}")


async def update_all():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(_executor, _update_all_sync)


@app.on_event("startup")
async def startup():
    await update_all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
