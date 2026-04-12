import requests
from datetime import datetime
from config import ALCHEMY_API_KEY, LARGE_TRANSFER_THRESHOLD_USD


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
    """获取ETH价格"""
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
        return r.json().get("ethereum", {}).get("usd", 0)
    except:
        return 0


def fetch_latest_transfers(limit=20):
    """获取最新大额转账"""
    from config import ALCHEMY_API_KEY
    if not ALCHEMY_API_KEY:
        print("[链上] 未配置ALCHEMY_API_KEY，跳过链上监控")
        return []

    eth_price = get_eth_price()
    if not eth_price:
        print("[链上] 无法获取ETH价格")
        return []

    # 获取最新区块
    block_num = _alchemy_request("eth_blockNumber")
    if not block_num:
        return []

    block_num = int(block_num, 16)
    events = []

    # 获取最近10个区块(带完整交易数据)
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

            if value_usd >= LARGE_TRANSFER_THRESHOLD_USD * 0.1:  # 10万美元以上
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
    """获取主流代币行情"""
    ids = "bitcoin,ethereum,binancecoin,solana,ripple,cardano,dogecoin,avalanche-2,polkadot,chainlink"
    names_map = {
        "bitcoin": "Bitcoin", "ethereum": "Ethereum", "binancecoin": "BNB",
        "solana": "Solana", "ripple": "XRP", "cardano": "Cardano",
        "dogecoin": "Dogecoin", "avalanche-2": "Avalanche",
        "polkadot": "Polkadot", "chainlink": "Chainlink",
    }
    symbol_map = {
        "bitcoin": "BTC", "ethereum": "ETH", "binancecoin": "BNB",
        "solana": "SOL", "ripple": "XRP", "cardano": "ADA",
        "dogecoin": "DOGE", "avalanche-2": "AVAX",
        "polkadot": "DOT", "chainlink": "LINK",
    }
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "sparkline": "false"},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        result = []
        for coin in data:
            cid = coin["id"]
            result.append({
                "symbol": symbol_map.get(cid, coin["symbol"].upper()),
                "name": names_map.get(cid, coin["name"]),
                "price": coin["current_price"],
                "change_24h": coin["price_change_percentage_24h"],
                "market_cap": coin["market_cap"],
            })
        print(f"[行情] 获取 {len(result)} 个代币")
        return result
    except Exception as e:
        print(f"[行情] 获取失败: {e}")
        return []
