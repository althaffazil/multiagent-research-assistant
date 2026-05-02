import os
from langchain_google_genai import ChatGoogleGenerativeAI
from state.schema import AgentState  # <--- Add this linte

def reviewer_agent(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
    
    last_message = state["messages"][-1].content
    plan = state["plan"]
    
    prompt = f"""Review the following research based on the original plan. 
    Plan: {plan}
    Research: {last_message}
    
    If the research is missing key points from the plan, provide specific critique. 
    If it is excellent, reply only with the word 'PASSED'."""
    
    response = llm.invoke(prompt)
    return {"critique": response.content}