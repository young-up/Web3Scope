import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone


RSS_FEEDS = [
    {"name": "The Block", "url": "https://www.theblock.co/rss.xml"},
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
    {"name": "Cointelegraph", "url": "https://cointelegraph.com/rss"},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def _fetch_rss(feed_info):
    try:
        feed = feedparser.parse(feed_info["url"])
        articles = []
        for entry in feed.entries[:10]:
            published = getattr(entry, "published_parsed", None)
            dt = datetime(*published[:6], tzinfo=timezone.utc).isoformat() if published else ""
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:300],
                "source": feed_info["name"],
                "published_at": dt,
            })
        return articles
    except Exception as e:
        print(f"[RSS] {feed_info['name']}: {e}")
        return []


def _fetch_panews():
    try:
        r = requests.get("https://www.panewslab.com/zh", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        articles = []
        for a in soup.find_all("a"):
            text = a.get_text(strip=True)
            href = a.get("href", "")
            if 10 < len(text) < 120 and href and not text.startswith("・"):
                link = href if href.startswith("http") else f"https://www.panewslab.com{href}"
                articles.append({"title": text, "link": link, "summary": "", "source": "PANews", "published_at": ""})
                if len(articles) >= 12:
                    break
        return articles
    except:
        return []


def _fetch_blockbeats():
    try:
        r = requests.get("https://www.theblockbeats.info/flash", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        articles = []
        for a in soup.find_all("a"):
            text = a.get_text(strip=True)
            href = a.get("href", "")
            if 15 < len(text) < 120 and href:
                link = href if href.startswith("http") else f"https://www.theblockbeats.info{href}"
                articles.append({"title": text, "link": link, "summary": "", "source": "BlockBeats", "published_at": ""})
                if len(articles) >= 10:
                    break
        return articles
    except:
        return []


def fetch_all_news():
    all_articles = []
    for feed_info in RSS_FEEDS:
        all_articles.extend(_fetch_rss(feed_info))
    all_articles.extend(_fetch_panews())
    all_articles.extend(_fetch_blockbeats())
    print(f"[新闻] 共获取 {len(all_articles)} 条")
    return all_articles
