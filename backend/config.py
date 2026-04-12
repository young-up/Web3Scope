import os
from dotenv import load_dotenv

load_dotenv()

# LLM配置
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_MODEL = os.getenv("LLM_MODEL", "glm-4.5")

# Alchemy配置
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "")

# Discord Webhook
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# 大额转账阈值(USD)
LARGE_TRANSFER_THRESHOLD_USD = 100_000  # 10万美元

# API配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
