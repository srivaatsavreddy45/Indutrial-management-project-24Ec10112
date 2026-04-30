from langgraph.graph import StateGraph, END
from .models import AgentState
from .nodes import *


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("ingestion", data_ingestion_node)
    g.add_node("analyst", market_analyst_node)
    g.add_node("forecast", forecasting_node)
    g.add_node("manager", executive_manager_node)

    g.set_entry_point("ingestion")

    g.add_edge("ingestion", "analyst")
    g.add_edge("analyst", "forecast")
    g.add_edge("forecast", "manager")
    g.add_edge("manager", END)

    return g.compile()


graph = build_graph()