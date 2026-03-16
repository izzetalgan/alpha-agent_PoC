# Alpha Agent: Quantitative Analysis Engine 📈

A multi-agent AI system built with **LangGraph** and **FastAPI** that acts as an automated quantitative research team. It evaluates financial assets and outputs structured, data-driven portfolio recommendations.

## 🧠 Architecture
This engine replaces standard conversational LLM prompt-chains with a Directed Acyclic Graph (DAG) for deterministic execution. 
- **News Agent:** Scrapes real-time financial news and extracts market sentiment (Bullish/Bearish/Neutral).
- **Fundamentals Agent:** Pulls live Yahoo Finance metrics (P/E, Market Cap) to assess intrinsic valuation.
- **Risk Agent:** Calculates technical indicators (50/200-day Moving Averages, 14-day RSI) directly from pandas dataframes.
- **Master Agent:** A synthesizer that uses a strict **70/30 Weighted Algorithm** (70% asset data quality, 30% client risk profile) to output a strict JSON decision (BUY/HOLD/SELL).

## 🚀 How to Run Locally

**1. Clone the repository and navigate to the directory:**
```bash
git clone <your-github-repo-url>
cd alpha-agent-poc