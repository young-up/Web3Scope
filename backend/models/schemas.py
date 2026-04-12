from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal


class ChainEvent(BaseModel):
    type: Literal["transfer", "dex_trade", "contract_deploy", "approval"]
    chain: str = "ethereum"
    hash: str = ""
    from_address: str = ""
    to_address: str = ""
    token: str = ""
    amount: float = 0
    amount_usd: float = 0
    timestamp: Optional[datetime] = None
    raw_data: dict = {}


class NewsArticle(BaseModel):
    title: str
    link: str = ""
    summary: str = ""
    source: str = ""
    published_at: str = ""


class PriceData(BaseModel):
    symbol: str
    price: float
    change_24h: float = 0


class AIAnalysis(BaseModel):
    event_type: str
    importance: Literal["high", "medium", "low"]
    summary: str
    insight: str


class DailyReport(BaseModel):
    date: str
    events: list[dict] = []
    news: list[dict] = []
    prices: list[dict] = []
    analysis: str = ""
