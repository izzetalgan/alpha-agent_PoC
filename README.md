# Alpha Agent: Quantitative Analysis Engine 📈

A multi-agent AI system built with **LangGraph** and **FastAPI** that acts as an automated quantitative research team. It evaluates financial assets and outputs structured, data-driven portfolio recommendations using institutional risk metrics.

## 🧠 Architecture (The Glass Box)
This engine replaces standard conversational LLM prompt-chains with a Directed Acyclic Graph (DAG) for deterministic, hallucination-free execution. 
- **News Agent:** Scrapes real-time financial news with fallback mechanisms to extract market sentiment (Bullish/Bearish/Neutral). It is strictly prompted to refuse to speculate if data is unavailable.
- **Fundamentals Agent:** Pulls live Yahoo Finance metrics (P/E, Market Cap) to assess intrinsic valuation against heuristic thresholds.
- **Risk Agent:** Calculates institutional-grade technicals directly from Pandas/NumPy dataframes, including **14-day RSI**, **Moving Averages (50/200)**, **Beta**, **1-Year Max Drawdown**, and the **Sharpe Ratio**.
- **Master Agent:** A synthesizer that uses a strict **70/30 Weighted Algorithm** (70% asset data quality, 30% client risk profile) to output a validated JSON decision (BUY/HOLD/SELL).

## 🚀 PoC vs. Production Roadmap
While this Proof of Concept uses static heuristics to prove the DAG architecture executes safely, the modular design is built for enterprise upgrades:
- **Decision Logic:** Upgrading the static 70/30 split to Modern Portfolio Theory (Mean-Variance Optimization).
- **Risk Metrics:** Dynamically pegging the Sharpe Ratio's risk-free rate to the live 10-Year Treasury Yield.
- **Momentum:** Pairing RSI with MACD to mathematically verify trend reversals.

## 💻 How to Run Locally

**1. Clone the repository and navigate to the directory:**
```bash
git clone [https://github.com/izzetalgan/alpha-agent_PoC.git](https://github.com/izzetalgan/alpha-agent_PoC.git)
cd alpha-agent_PoC