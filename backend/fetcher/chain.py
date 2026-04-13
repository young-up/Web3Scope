import requests
import time
from datetime import datetime
from config import ALCHEMY_API_KEY, LARGE_TRANSFER_THRESHOLD_USD

# 简单缓存，避免频繁请求外部API
_price_cache = {"data": None, "eth_price": None, "timestamp": 0}
_CACHE_TTL = 300  # 5分钟缓存


def _alchemy_request(method, params=None):
    """调用Alchemy API"""
    if not ALCHEMY_API_KEY:
        return None
    url = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    payload = {"jsonrpc": "2.0", "method": method, "id": 1}
    if params:
        payload["params"] = params
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.json().get("result")
    except Exception as e:
        print(f"[Alchemy] 请求失败: {e}")
        return None


def get_eth_price():
    """获取ETH价格（Coinbase API）"""
    if _price_cache["eth_price"] and time.time() - _price_cache["timestamp"] < _CACHE_TTL:
        return _price_cache["eth_price"]
    try:
        r = requests.get("https://api.exchange.coinbase.com/products/ETH-USD/ticker", timeout=10)
        price = float(r.json()["price"])
        _price_cache["eth_price"] = price
        _price_cache["timestamp"] = time.time()
        return price
    except:
        return _price_cache.get("eth_price") or 0


def fetch_latest_transfers(limit=20):
    """获取最新大额转账"""
    if not ALCHEMY_API_KEY:
        print("[链上] 未配置ALCHEMY_API_KEY，跳过链上监控")
        return []

    eth_price = get_eth_price()
    if not eth_price:
        print("[链上] 无法获取ETH价格")
        return []

    block_num = _alchemy_request("eth_blockNumber")
    if not block_num:
        return []

    block_num = int(block_num, 16)
    events = []

    for offset in range(10):
        block = _alchemy_request("eth_getBlockByNumber", [hex(block_num - offset), True])
        if not block:
            continue

        block_time = datetime.fromtimestamp(int(block["timestamp"], 16))

        for tx in block.get("transactions", [])[:100]:
            if not isinstance(tx, dict) or not tx.get("to") or not tx.get("from"):
                continue

            value_eth = int(tx.get("value", "0x0"), 16) / 1e18
            value_usd = value_eth * eth_price

            if value_usd >= LARGE_TRANSFER_THRESHOLD_USD * 0.1:
                events.append({
                    "type": "transfer",
                    "chain": "ethereum",
                    "hash": tx.get("hash", ""),
                    "from_address": tx["from"],
                    "to_address": tx["to"],
                    "token": "ETH",
                    "amount": round(value_eth, 4),
                    "amount_usd": round(value_usd, 2),
                    "timestamp": block_time.isoformat(),
                })

    print(f"[链上] 获取 {len(events)} 条大额转账")
    return events[:limit]


def fetch_top_tokens():
    """获取主流代币行情（Coinbase API，免费无限流）"""
    if _price_cache["data"] and time.time() - _price_cache["timestamp"] < _CACHE_TTL:
        return _price_cache["data"]

    pairs = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD",
             "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "LINK-USD"]
    names = {"BTC": "Bitcoin", "ETH": "Ethereum", "BNB": "BNB", "SOL": "Solana",
             "XRP": "XRP", "ADA": "Cardano", "DOGE": "Dogecoin", "AVAX": "Avalanche",
             "DOT": "Polkadot", "LINK": "Chainlink"}
    try:
        result = []
        for pair in pairs:
            try:
                r = requests.get(f"https://api.exchange.coinbase.com/products/{pair}/ticker", timeout=10)
                d = r.json()
                sym = pair.replace("-USD", "")
                result.append({
                    "symbol": sym,
                    "name": names.get(sym, sym),
                    "price": float(d["price"]),
                    "change_24h": float(d.get("price_24h_change", 0)) if d.get("price_24h_change") else 0,
                    "market_cap": 0,
                })
            except:
                continue
            time.sleep(0.1)  # 避免太快
        print(f"[行情] 获取 {len(result)} 个代币")
        _price_cache["data"] = result
        _price_cache["timestamp"] = time.time()
        return result
    except Exception as e:
        print(f"[行情] 获取失败: {e}")
        return _price_cache.get("data") or []
