import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import search_news, get_stock_fundamentals, get_price_history

# Load the Groq API key from our .env file
load_dotenv()

# 1. Initialize the Core Engine (Llama 3.1 via Groq)
# We use temperature=0.2 to keep the agents analytical and prevent "hallucinations"
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=1024
)

# 2. Bind the specific tools to the specific agents
# This ensures the News agent doesn't try to calculate math, and the Risk agent doesn't read the news.
news_llm = llm.bind_tools([search_news])
fundamentals_llm = llm.bind_tools([get_stock_fundamentals])
risk_llm = llm.bind_tools([get_price_history])

# Define the strict JSON structure
class MasterDecision(BaseModel):
    action: str = Field(description="Strictly BUY, HOLD, or SELL")
    confidence_score: int = Field(description="Confidence score from 0 to 100")
    key_driver: str = Field(description="The primary driver: Fundamentals, News, or Risk")
    reasoning: str = Field(description="Detailed explanation of the 70/30 weighted logic")

# Force the Master Agent to output ONLY this structure
master_llm = llm.with_structured_output(MasterDecision)

# 3. Define the System Prompts
NEWS_PROMPT = """You are the Senior Financial News Analyst.
Your job is to read the provided raw news data and extract the true market sentiment.

INSTRUCTIONS:
1. Identify the core narrative (e.g., earnings beat, macro-economic headwinds, new product launches).
2. Assess the overall sentiment as strictly BULLISH, BEARISH, or NEUTRAL.
3. Ignore marketing fluff. Focus on verifiable events that actually move stock prices.
4. Note the recency of the news. Old news is irrelevant.

Output a concise, hard-hitting summary of the current news cycle for this asset."""

FUNDAMENTALS_PROMPT = """You are the Lead Fundamental Valuation Analyst.
Your job is to evaluate the company's intrinsic value based on the provided metrics.

INSTRUCTIONS:
1. Analyze the P/E Ratio. A high P/E (e.g., > 30) often indicates it is overvalued or a high-growth tech stock. A low P/E (e.g., < 15) might indicate it is undervalued or a stagnant company.
2. Consider the Market Cap to understand the company's size, liquidity, and stability.
3. Contextualize the numbers based on its Sector (e.g., Tech typically commands higher P/E ratios than Utilities).

Output a strict verdict on whether the asset is currently OVERVALUED, UNDERVALUED, or FAIRLY VALUED, and explain the mathematical reasoning."""

RISK_PROMPT = """You are the Chief Risk Officer and Quantitative Analyst.
Your job is to evaluate the asset's technical momentum and institutional risk profile.

INSTRUCTIONS:
1. Technical Trend: Compare Current Price to the 50-Day and 200-Day Moving Averages.
2. Momentum: Analyze the 14-Day RSI. Warn explicitly if it is Overbought (>70) or Oversold (<30).
3. Institutional Risk:
   - Evaluate Beta: Is it highly volatile (>1.0) or stable (<1.0)?
   - Evaluate Max Drawdown: How severe was the worst crash this year?
   - Evaluate Sharpe Ratio: Is the asset generating good returns relative to its risk (>1.0)?

Output a precise, institutional-grade technical and risk assessment. Conclude if the asset is fundamentally safe or highly speculative."""

MASTER_PROMPT = """You are the Lead Quantitative Portfolio Manager (The Glass Box Engine).
You have received independent analyses from your News, Fundamentals, and Risk agents regarding the ticker: {ticker}.

Here are the reports:
---
NEWS AGENT:
{news_report}

FUNDAMENTALS AGENT:
{fundamentals_report}

RISK AGENT:
{risk_report}
---

CLIENT PROFILE: {client_profile}

INSTRUCTIONS FOR SYNTHESIS:
Act as a cold, calculating quantitative analyst. Do not automatically output BUY for Aggressive or SELL for Conservative. You must use a weighted logic system:

1. Base Asset Quality (70% Weight): Evaluate the fundamental valuation, geopolitical news, and price momentum from the reports. Is this a mathematically sound investment right now?
2. Profile Adjustment (30% Weight): Use the '{client_profile}' profile strictly as a risk-tolerance modifier. For example, a Conservative client can still get a 'BUY' rating if the stock is deeply undervalued and safe. An Aggressive client should get a 'SELL' if the asset's fundamentals are collapsing.

Synthesize this data and output a final decision (BUY, HOLD, or SELL). 
Explain your reasoning clearly, explicitly mentioning how the asset's raw data (70%) interacted with the client's risk profile (30%) to reach your conclusion."""