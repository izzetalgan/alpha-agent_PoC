import yfinance as yf
import pandas as pd
import numpy as np

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from functools import lru_cache
from duckduckgo_search import DDGS

# News Tool
@tool
def search_news(ticker: str) -> str:
    """Searches strictly for the latest financial news, with a fallback to general search."""
    try:
        query = f"{ticker} stock market financial news"
        
        # 1. Try the strict News tab first
        results = DDGS().news(keywords=query, max_results=5)
        
        # 2. FALLBACK: If news tab is empty or blocked, try general web search
        if not results:
            results = DDGS().text(keywords=query, max_results=5)
            
        if not results:
            return f"No recent news found for {ticker} on any search index."
            
        formatted_news = ""
        for i, article in enumerate(results):
            formatted_news += f"[{i+1}] Title: {article.get('title', 'No Title')}\n"
            formatted_news += f"Snippet: {article.get('body', 'No snippet')}\n\n"
            
        return formatted_news
        
    except Exception as e:
        return f"Error fetching news: {str(e)}. Proceed with available context."

@tool
@lru_cache(maxsize=10)
def get_stock_fundamentals(ticker: str) -> str:
    """Fetches key fundamental data with aggressive error fallbacks."""
    try:
        stock = yf.Ticker(ticker)
        # Force info to be an empty dictionary if Yahoo fails to return it
        info = stock.info or {} 
        
        pe_ratio = info.get('forwardPE', info.get('trailingPE', 'Data Unavailable'))
        market_cap = info.get('marketCap', 'Data Unavailable')
        sector = info.get('sector', 'Unknown Sector')
        
        return f"Sector: {sector} | Market Cap: {market_cap} | P/E Ratio: {pe_ratio}"
    except Exception as e:
        return f"Error fetching fundamentals: {str(e)}. Proceed with available context."


# Upgraded Risk Tool (With Moving Averages & Error Handling)
@tool
@lru_cache(maxsize=10)
def get_price_history(ticker: str) -> str:
    """Fetches price action, Technicals (RSI, MAs), and Institutional Risk Metrics (Sharpe, Max Drawdown, Beta)."""
    try:
        stock = yf.Ticker(ticker)
        
        # Fetch 1 year of data for institutional risk metrics
        hist = stock.history(period="1y")
        if hist.empty or len(hist) < 20:
            return "Insufficient price history available for this ticker."
            
        # 1. Basic Price Action & Info
        end_price = hist['Close'].iloc[-1]
        info = stock.info or {}
        ma_50 = info.get('fiftyDayAverage', 'N/A')
        ma_200 = info.get('twoHundredDayAverage', 'N/A')
        beta = info.get('beta', 'N/A')
        
        # 2. Calculate 14-Day RSI (Relative Strength Index)
        delta = hist['Close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -1 * delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # 3. Calculate Maximum Drawdown (1 Year)
        rolling_max = hist['Close'].cummax()
        drawdowns = (hist['Close'] / rolling_max) - 1.0
        max_drawdown = drawdowns.min() * 100 # Convert to percentage

        # 4. Calculate Annualized Sharpe Ratio (Assuming 4% Risk-Free Rate)
        daily_returns = hist['Close'].pct_change().dropna()
        risk_free_rate_daily = 0.04 / 252 # 4% divided by 252 trading days
        excess_returns = daily_returns - risk_free_rate_daily
        
        # Avoid division by zero if standard deviation is 0
        std_dev = excess_returns.std()
        if std_dev != 0:
            sharpe_ratio = np.sqrt(252) * (excess_returns.mean() / std_dev)
        else:
            sharpe_ratio = 0.0

        # Construct the final institutional report
        report = (
            f"Current Close: ${end_price:.2f}\n"
            f"50-Day MA: ${ma_50} | 200-Day MA: ${ma_200}\n"
            f"14-Day RSI: {current_rsi:.2f} (Note: >70 is Overbought, <30 is Oversold)\n"
            f"--- INSTITUTIONAL RISK METRICS ---\n"
            f"Beta: {beta} (Note: >1 means more volatile than the market)\n"
            f"Max Drawdown (1Y): {max_drawdown:.2f}%\n"
            f"Sharpe Ratio (1Y): {sharpe_ratio:.2f} (Note: >1.0 is good risk-adjusted return)\n"
        )
        return report
    except Exception as e:
        return f"Error fetching price history: {str(e)}. Proceed with available context."