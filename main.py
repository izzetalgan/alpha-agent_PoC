from graph import app

def main():
    print("\n" + "="*50)
    print(" ALPHA AGENT PoC TERMINAL ")
    print("="*50)
    
    while True:
        print("\n" + "-"*50)
        ticker = input("Enter a stock ticker to analyze (e.g., AAPL, NVDA, TSLA) or 'exit' to quit: ").strip().upper()
        
        if ticker.lower() in ['exit', 'quit']:
            print("Shutting down the engine. Goodbye!")
            break
            
        if not ticker:
            continue

        print("\nSelect Client Risk Profile:")
        print("1. Conservative (Focus on capital preservation, low risk)")
        print("2. Balanced (Moderate risk and reward)")
        print("3. Aggressive (High risk tolerance, growth-focused)")
        
        profile_choice = input("Enter 1, 2, or 3: ").strip()
        profiles = {
            "1": "Conservative",
            "2": "Balanced",
            "3": "Aggressive"
        }
        client_profile = profiles.get(profile_choice, "Balanced") # Defaults to Balanced if typo

        print(f"\n[!] Initiating Agent Swarm for {ticker} | Profile: {client_profile}...\n")

        # This is the initial GraphState payload we send into the START node
        initial_state = {
            "ticker": ticker,
            "client_profile": client_profile,
            "news_report": "",
            "fundamentals_report": "",
            "risk_report": "",
            "final_decision": ""
        }

        try:
            # .invoke() runs the LangGraph engine from START to END
            result = app.invoke(initial_state)
            
            # The 'result' contains the final GraphState, including the Master Agent's output
            print("\n" + "="*50)
            print(f" FINAL MASTER AGENT DECISION FOR {ticker} ")
            print("="*50)
            print(result['final_decision'])
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"\n❌ An error occurred during execution: {e}\n")

if __name__ == "__main__":
    main()