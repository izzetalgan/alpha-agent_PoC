from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Import our LLM, prompts, and tools
from agents import llm, master_llm, NEWS_PROMPT, FUNDAMENTALS_PROMPT, RISK_PROMPT, MASTER_PROMPT
from tools import search_news, get_stock_fundamentals, get_price_history

# 1. Define the State (The shared memory payload passed between nodes)
class GraphState(TypedDict):
    ticker: str
    client_profile: str
    news_report: str
    fundamentals_report: str
    risk_report: str
    final_decision: str

# 2. Define the Nodes (The execution blocks)
def news_node(state: GraphState):
    """Fetches news data and asks the News Agent to summarize it."""
    print(f"📰 News Agent analyzing {state['ticker']}...")
    raw_data = search_news.invoke(state['ticker'] + " stock news")
    prompt = NEWS_PROMPT + f"\n\nTicker: {state['ticker']}\nRaw Data Context:\n{raw_data}"
    
    response = llm.invoke(prompt)
    return {"news_report": response.content}

def fundamentals_node(state: GraphState):
    """Fetches financial data and asks the Fundamentals Agent to analyze it."""
    print(f"📊 Fundamentals Agent analyzing {state['ticker']}...")
    raw_data = get_stock_fundamentals.invoke(state['ticker'])
    prompt = FUNDAMENTALS_PROMPT + f"\n\nTicker: {state['ticker']}\nRaw Data Context:\n{raw_data}"
    
    response = llm.invoke(prompt)
    return {"fundamentals_report": response.content}

def risk_node(state: GraphState):
    """Fetches price history and asks the Risk Agent to evaluate it."""
    print(f"⚠️ Risk Agent analyzing {state['ticker']}...")
    raw_data = get_price_history.invoke(state['ticker'])
    prompt = RISK_PROMPT + f"\n\nTicker: {state['ticker']}\nRaw Data Context:\n{raw_data}"
    
    response = llm.invoke(prompt)
    return {"risk_report": response.content}

def master_node(state: GraphState):
    """Synthesizes the 3 reports into a structured final decision."""
    print(f"🧠 Master Agent calculating 70/30 weighted decision for {state['client_profile']} profile...")
    
    prompt = MASTER_PROMPT.format(
        ticker=state['ticker'],
        client_profile=state['client_profile'],
        news_report=state['news_report'],
        fundamentals_report=state['fundamentals_report'],
        risk_report=state['risk_report']
    )
    
    # Notice we are calling master_llm here, not llm!
    response = master_llm.invoke(prompt)
    
    # response is now a Pydantic object, not raw text. 
    # Let's format it beautifully so your React UI can display it safely:
    formatted_decision = (
        f"🎯 ACTION: {response.action}\n"
        f"📊 CONFIDENCE: {response.confidence_score}%\n"
        f"🔑 KEY DRIVER: {response.key_driver}\n\n"
        f"🧠 REASONING:\n{response.reasoning}"
    )
    
    return {"final_decision": formatted_decision}

# 3. Build the Directed Acyclic Graph (DAG)
workflow = StateGraph(GraphState)

# Add our nodes to the graph
workflow.add_node("news_agent", news_node)
workflow.add_node("fundamentals_agent", fundamentals_node)
workflow.add_node("risk_agent", risk_node)
workflow.add_node("master_agent", master_node)

# Define the Routing (Edges)
# The 3 sub-agents start simultaneously (Parallel Execution)
workflow.add_edge(START, "news_agent")
workflow.add_edge(START, "fundamentals_agent")
workflow.add_edge(START, "risk_agent")

# Once they all finish, they pass their outputs to the Master Agent
workflow.add_edge("news_agent", "master_agent")
workflow.add_edge("fundamentals_agent", "master_agent")
workflow.add_edge("risk_agent", "master_agent")

# Master Agent finishes the process
workflow.add_edge("master_agent", END)

# 4. Compile the application
app = workflow.compile()