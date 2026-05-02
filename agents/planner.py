import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from state.schema import AgentState

load_dotenv()

def planner_agent(state: AgentState):
    # Pass the key explicitly to bypass validation errors
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    user_query = state['messages'][-1].content
    prompt = f"Create a 3-point research outline for: {user_query}"
    
    response = llm.invoke(prompt)
    return {"plan": response.content, "messages": [response]}