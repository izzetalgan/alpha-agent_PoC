# Alpha Agent: Quantitative Analysis Engine 📈

A multi-agent AI system built with **LangGraph** and **FastAPI** that acts as an automated quantitative research team. It evaluates financial assets and outputs structured, data-driven portfolio recommendations using institutional risk metrics.

## 🛠️ Core Technologies & Data Sources
We built this engine to prioritize backend logic, deterministic routing, and high-speed inference over basic chat interfaces.
- **AI Inference (Groq API):** Powered by the `Llama 3.3 70B` model running on Groq's LPU architecture for ultra-low latency reasoning.
- **Orchestration:** `LangGraph` is used to build a Directed Acyclic Graph (DAG), replacing standard linear prompt-chains with parallel agent execution.
- **Market Data:** `yfinance` is used to pull live market caps, P/E ratios, and historical price action.
- **Financial News:** `duckduckgo-search` library is used to scrape live journalism with built-in fallbacks.
- **Quantitative Math:** `Pandas` and `NumPy` handle the dataframe manipulation for technical indicators.

## 🧠 Architecture (The Glass Box)
This engine eliminates LLM hallucinations by forcing parallel execution and strictly validating outputs via Pydantic JSON schemas.
- **News Agent:** Scrapes real-time financial news to extract market sentiment (Bullish/Bearish/Neutral). It is strictly prompted to refuse to speculate if data is unavailable.
- **Fundamentals Agent:** Pulls live Yahoo Finance metrics to assess intrinsic valuation against heuristic thresholds.
- **Risk Agent:** Calculates institutional-grade technicals directly from Pandas dataframes, including **14-day RSI**, **Moving Averages (50/200)**, **Beta**, **1-Year Max Drawdown**, and the **Sharpe Ratio**.
- **Master Agent:** A synthesizer that uses a strict **70/30 Weighted Algorithm** (70% asset data quality, 30% client risk profile) to output a validated JSON decision (BUY/HOLD/SELL).

## 🚀 PoC vs. Production Roadmap
While this Proof of Concept uses static heuristics to prove the DAG architecture executes safely, the modular design is built for enterprise upgrades:
- **Decision Logic:** Upgrading the static 70/30 split to Modern Portfolio Theory (Mean-Variance Optimization).
- **Risk Metrics:** Dynamically pegging the Sharpe Ratio's risk-free rate to the live 10-Year Treasury Yield.
- **Momentum:** Pairing RSI with MACD to mathematically verify trend reversals.

## 💻 How to Run Locally


```bash
**1. Clone the repository:**
git clone [https://github.com/izzetalgan/alpha-agent_PoC.git](https://github.com/izzetalgan/alpha-agent_PoC.git)
cd alpha-agent_PoC

**2. Set up the virtual environment:**
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

**3. Get and add your API Key:**
Go to console.groq.com and create a free account to generate an API key.
Create a .env file in the root directory of this project and add your key:
GROQ_API_KEY=your_api_key_here

**4. Launch the System:**
./start.sh

Open your browser to http://localhost:8080 to interact with the engine.