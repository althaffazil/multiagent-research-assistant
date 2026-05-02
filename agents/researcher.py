import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from state.schema import AgentState

load_dotenv()

def researcher_agent(state: AgentState):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    plan = state.get("plan", "")
    critique = state.get("critique", "")
    
    # If there is a critique from the reviewer, address it
    if critique and "PASSED" not in critique:
        prompt = f"Your previous research was critiqued: {critique}. Please rewrite the report to address these issues based on the plan: {plan}"
    else:
        prompt = f"Based on this approved plan: {plan}, write a comprehensive research report in Markdown format."
    
    response = llm.invoke(prompt)
    # Return as a list so 'add_messages' can append it to the history
    return {"messages": [response]}