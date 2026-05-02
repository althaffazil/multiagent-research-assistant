from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state.schema import AgentState
from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.reviewer import reviewer_agent

def should_continue(state: AgentState):
    if state.get("critique") and "PASSED" in state["critique"]:
        return END
    return "researcher"

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_agent)
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("reviewer", reviewer_agent)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "reviewer")

    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "researcher": "researcher",
            END: END
        }
    )

    return workflow.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["researcher"]
    )