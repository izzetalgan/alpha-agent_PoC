# Alpha Agent: A Multi-Agent Quantitative Evaluation Engine
**A Proof-of-Concept for Deterministic Financial Analysis using LangGraph**

## 1. Abstract
The current landscape of automated financial research is polarized. On one end, traditional algorithmic screeners rely on rigid rulesets that cannot interpret qualitative market sentiment. On the other end, modern Large Language Models (LLMs) possess deep contextual understanding but are prone to non-deterministic outputs and "hallucinations," making them unsafe for direct financial deployment. 

The Alpha Agent project bridges this gap by introducing a multi-agent Directed Acyclic Graph (DAG) architecture. By isolating specific analytical tasks into distinct agent personas and strictly constraining their outputs using JSON schemas, this Proof-of-Concept (PoC) demonstrates how LLMs can be utilized safely in wealth management. The engine synthesizes hard quantitative data with a predefined client risk profile to generate deterministic, mathematically grounded investment recommendations.

## 2. Data Infrastructure & API Integrations
To ensure high reliability and eliminate hallucinations, the system does not rely on the LLM's internal memory. Instead, it acts as a reasoning engine over live, external data pipelines:

* **Inference Engine (Groq API):** The core reasoning is powered by the `Llama 3.3 70B` model, accessed via the Groq API. Groq's LPU (Language Processing Unit) architecture was specifically chosen to provide the ultra-low latency required for real-time financial analysis.
* **Quantitative Data (Yahoo Finance):** The Python `yfinance` library is used to programmatically fetch live market caps, P/E ratios, and historical price action directly from Yahoo's servers.
* **Qualitative Data (DuckDuckGo Search):** Real-time financial journalism is scraped using the `duckduckgo-search` API. 
* **System Resilience:** To prevent IP bans and reduce network latency, the Python backend implements `lru_cache` for memory management. Furthermore, aggressive `try/except` fallbacks ensure that if an external API fails, the AI degrades gracefully and refuses to speculate.

## 3. System Architecture: The "Glass Box" Model
Standard LLM applications use linear prompt-chaining, which creates a "black box" where errors compound silently. Alpha Agent is built on **LangGraph**, replacing open-ended chat functionality with a structured DAG execution pipeline. 

### 3.1 The Sub-Agent Layer (Parallel Execution)
The system utilizes three specialized sub-agents running concurrently. Each agent is strictly prompted to stay within its domain:
* **The Fundamentals Agent:** Evaluates intrinsic valuation using live P/E ratios and Market Cap data.
* **The Risk Agent:** Operates purely on mathematical data. Using `pandas` and `numpy`, the Python backend calculates technical indicators and risk metrics. The LLM is restricted to interpreting these hard calculations rather than generating its own technical analysis.
* **The News Agent:** Measures qualitative momentum by parsing recent financial journalism, actively filtering out marketing noise to establish market sentiment.

### 3.2 The Master Synthesis Agent (Constraint-Based Logic)
Once the sub-agents complete their localized processing, their formatted reports are passed to the Master Agent. To prevent arbitrary choices, the Master Agent is bound by a strict **70/30 Weighted Algorithm**:
* **70% Asset Quality:** The combined data-driven insights of the sub-agents.
* **30% Client Risk Profile:** A hard constraint (e.g., Conservative, Balanced, Aggressive) injected into the prompt. 

This algorithm forces the Master Agent to act as a fiduciary. For example, high volatility metrics will trigger the 30% client safety constraint for a Conservative user, mathematically forcing the system to output a "SELL" or "HOLD" decision, even if the asset shows high growth potential.

## 4. Quantitative Methodology: The PoC vs. Production Roadmap
To build a functional engine within the constraints of a PoC, the Alpha Agent relies on established financial heuristics. However, the modular architecture is designed so these static rules can be seamlessly swapped for institutional-grade algorithms in production.

### 4.1 Macro-Trend & Momentum Indicators
* **The PoC Implementation:** The engine calculates **50-Day and 200-Day Simple Moving Averages (SMA)** for macro-trends, and the **14-Day Relative Strength Index (RSI)** for momentum.
* **The Production Upgrade:** Because SMAs are lagging indicators, a production environment would utilize **Exponential Moving Averages (EMA)** or **Volume-Weighted Average Price (VWAP)** to react faster to sudden market shifts. The RSI would be paired with **Bollinger Bands** or **MACD** to mathematically verify trend reversals.

### 4.2 Institutional Risk Metrics
Wealth managers evaluate risk-adjusted returns, not just absolute gains. The backend calculates two critical metrics:
* **Maximum Drawdown:** Assesses the worst-case historical drop over 1 year. 
$$MDD = \frac{Trough - Peak}{Peak}$$
* **Sharpe Ratio:** Measures return against volatility, assuming a static 4% risk-free rate for the PoC.
$$Sharpe = \frac{R_p - R_f}{\sigma_p}$$
* **The Production Upgrade:** A live institutional system would dynamically peg the risk-free rate to the live **10-Year Treasury Yield** via an API and calculate the **Sortino Ratio** to exclusively measure downside volatility.

### 4.3 Decision Weighting
* **The PoC Implementation:** The hardcoded 70/30 (Asset/Profile) split proves the LLM can follow rigid constraints.
* **The Production Upgrade:** In an enterprise environment, this static ratio would be replaced by **Modern Portfolio Theory (Mean-Variance Optimization)**, plotting the client's exact risk tolerance on an Efficient Frontier curve.

## 5. Conclusion
The Alpha Agent project demonstrates that the inherent unpredictability of Large Language Models can be successfully managed for institutional finance. By stripping the AI of its ability to "guess" mathematical outcomes and instead forcing it to synthesize hard data from deterministic APIs (Groq, Yahoo Finance), the engine provides safe, logical, and profile-adjusted financial recommendations.