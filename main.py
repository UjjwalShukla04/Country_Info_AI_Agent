import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import AgentState
from nodes import identify_intent, invoke_tool, synthesize_answer

# Define the graph
def create_graph():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("identify_intent", identify_intent)
    workflow.add_node("invoke_tool", invoke_tool)
    workflow.add_node("synthesize_answer", synthesize_answer)

    # Add edges
    workflow.add_edge(START, "identify_intent")
    
    # Conditional edge could be added here to skip tool if intent failed
    # For now, we handle error state in the next node
    workflow.add_edge("identify_intent", "invoke_tool")
    
    workflow.add_edge("invoke_tool", "synthesize_answer")
    workflow.add_edge("synthesize_answer", END)

    # Compile the graph
    app = workflow.compile()
    return app

def main():
    """
    Main entry point for the CLI.
    """
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it in a .env file or export it in your shell.")
        return

    app = create_graph()
    
    print("Country Information AI Agent (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print("Agent: Processing...")
        
        try:
            initial_state = {"question": user_input, "messages": []}
            result = app.invoke(initial_state)
            
            print(f"Agent: {result['answer']}")
            if result.get("error"):
                print(f"Debug Info - Error: {result['error']}")
                
        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
