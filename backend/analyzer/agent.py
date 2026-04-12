from openai import OpenAI
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


def _create_client():
    return OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)


ANALYSIS_PROMPT = """你是Web3链上数据分析师。分析以下链上事件，判断重要程度并给出见解。

事件数据：
{events}

规则：
- 🔴重要：>500万美元转账、知名地址、可能影响市场的事件
- 🟡值得关注：100-500万美元、有分析价值的事件
- 🟢一般：其他事件

对每条事件输出JSON数组格式：
[{{"hash":"0x...","importance":"high/medium/low","summary":"一句话摘要","insight":"为什么重要"}}]

只输出JSON，不要其他内容。"""


def analyze_events(events):
    """分析链上事件"""
    if not events:
        return []

    client = _create_client()
    events_text = "\n".join([
        f"- {e.get('type','')} | {e.get('token','ETH')} {e.get('amount',0):.2f} (${e.get('amount_usd',0):,.0f}) | {e.get('from_address','')}→{e.get('to_address','')} | {e.get('hash','')}"
        for e in events
    ])

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是链上数据分析专家，擅长识别异常交易和市场信号。直接输出JSON。"},
                {"role": "user", "content": ANALYSIS_PROMPT.format(events=events_text)},
            ],
            temperature=0.2,
            max_tokens=2000,
        )
        content = response.choices[0].message.content or ""

        # 提取JSON
        import json
        import re
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return []
    except Exception as e:
        print(f"[AI分析] 失败: {e}")
        return []


DAILY_REPORT_PROMPT = """你是Web3行业分析师。根据以下数据生成中文日报，直接输出日报正文，不要分析过程。

## 链上重要事件
{events}

## 新闻（共{news_count}条）
{news}

## 行情
{prices}

要求：
1. 按主题分类，标注重要程度（🔴重要 / 🟡值得关注 / 🟢一般）
2. 每条1-2句话
3. 最后2-3句市场总结
4. 800-1200字"""


def generate_daily_report(events, news, prices):
    """生成每日日报"""
    client = _create_client()

    events_text = "\n".join([
        f"- {e.get('token','ETH')} {e.get('amount',0):.2f} (${e.get('amount_usd',0):,.0f}) {e.get('from_address','')[:10]}...→{e.get('to_address','')[:10]}..."
        for e in events[:20]
    ]) or "暂无大额事件"

    news_text = "\n".join([f"- [{n['source']}] {n['title']}" for n in news[:30]]) or "暂无新闻"

    prices_text = "\n".join([
        f"- {p['symbol']}: ${p['price']:,.2f} ({'📈' if p['change_24h']>=0 else '📉'} {p['change_24h']:.2f}%)"
        for p in prices
    ]) or "暂无行情数据"

    prompt = DAILY_REPORT_PROMPT.format(
        events=events_text, news_count=len(news),
        news=news_text, prices=prices_text
    )

    print("[AI] 正在生成日报...")
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是专业的Web3行业分析师。直接输出日报正文。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4000,
        )
        content = response.choices[0].message.content or ""
        # 跳过思考过程
        for marker in ["# Web3", "## DeFi", "## 📰", "## 链上"]:
            idx = content.find(marker)
            if idx > 0:
                content = content[idx:]
                break
        print(f"[AI] 日报生成完成，{len(content)}字")
        return content
    except Exception as e:
        print(f"[AI] 日报生成失败: {e}")
        return ""
