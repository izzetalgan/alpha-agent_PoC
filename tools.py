import yfinance as yf
import pandas as pd

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from functools import lru_cache
from duckduckgo_search import DDGS

# 1. News Tool
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
# 3. Upgraded Risk Tool (With Moving Averages & Error Handling)
@tool
@lru_cache(maxsize=10)
def get_price_history(ticker: str) -> str:
    """Fetches price action, Moving Averages, and the RSI indicator."""
    try:
        stock = yf.Ticker(ticker)
        
        # We fetch 3 months of data to ensure we have enough days to calculate a 14-day RSI
        hist = stock.history(period="3mo")
        if hist.empty:
            return "No price history available for this ticker."
            
        # 1. Price Action
        start_price = hist['Close'].iloc[-21] # Approx 1 month ago
        end_price = hist['Close'].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        
        # 2. Moving Averages
        info = stock.info
        ma_50 = info.get('fiftyDayAverage', 'N/A')
        ma_200 = info.get('twoHundredDayAverage', 'N/A')
        
        # 3. Calculate 14-Day RSI (Relative Strength Index)
        delta = hist['Close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -1 * delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        report = (
            f"Current Close: ${end_price:.2f}\n"
            f"1-Month Change: {percent_change:.2f}%\n"
            f"50-Day MA: ${ma_50}\n"
            f"200-Day MA: ${ma_200}\n"
            f"14-Day RSI: {current_rsi:.2f}\n"
            f"(Note: RSI > 70 is Overbought/Bearish. RSI < 30 is Oversold/Bullish.)"
        )
        return report
    except Exception as e:
        return f"Error fetching price history: {str(e)}. Proceed with available context."