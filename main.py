import os
import uuid
from dotenv import load_dotenv

# MUST be the first thing called
load_dotenv()

from graph.builder import build_graph

def main():
    app = build_graph()
    
    # Unique thread ID for this specific research session
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    query = input("Enter your research topic: ")
    inputs = {"messages": [("user", query)]}

    print("\n--- Generating Plan... ---")
    for event in app.stream(inputs, config, stream_mode="values"):
        if "plan" in event:
            print(f"\nPROPOSED PLAN:\n{event['plan']}")

    # Graph is now paused.
    confirm = input("\nApprove this plan? (yes/no): ").lower()

    if confirm == "yes":
        print("\n--- Running Final Research... ---")
        # Passing None resumes from the breakpoint
        for event in app.stream(None, config, stream_mode="values"):
            final_content = event["messages"][-1].content
        
        print("\nRESEARCH COMPLETE:")
        print(final_content)
    else:
        print("Workflow terminated. Try a different query.")

if __name__ == "__main__":
    main()