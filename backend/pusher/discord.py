import requests
from config import DISCORD_WEBHOOK_URL


def push_discord_embed(title, content):
    if not DISCORD_WEBHOOK_URL:
        return False
    try:
        chunks = []
        lines = content.split("\n")
        current = ""
        for line in lines:
            if len(current) + len(line) + 1 > 3900:
                chunks.append(current.strip())
                current = ""
            current += line + "\n"
        if current.strip():
            chunks.append(current.strip())

        for i, chunk in enumerate(chunks):
            embed = {
                "description": chunk,
                "color": 5814783,
                "footer": {"text": f"Web3Scope • {i+1}/{len(chunks)}"} if len(chunks) > 1 else {"text": "Web3Scope"},
            }
            if i == 0:
                embed["title"] = title
            resp = requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]}, timeout=10)
            print(f"[Discord] 分段{i+1}/{len(chunks)}: {resp.status_code}")
        return True
    except Exception as e:
        print(f"[Discord] 推送失败: {e}")
        return False


def push_discord_alert(title, description, color=16776960):
    """推送紧急告警(黄色)"""
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={
            "embeds": [{"title": f"⚠️ {title}", "description": description, "color": color, "footer": {"text": "Web3Scope Alert"}}]
        }, timeout=10)
    except:
        pass
