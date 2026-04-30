from .models import AgentState


def data_ingestion_node(state: AgentState):
    return {"messages": ["INTAKE: Data received"]}


def market_analyst_node(state: AgentState):
    return {
        "market_signal": "Demand surge detected",
        "messages": ["ANALYST: Positive signal"]
    }


def forecasting_node(state: AgentState):
    history = state["historical_sales"]

    if not history:
        return {"forecast_value": 0, "messages": ["FORECAST: No data"]}

    avg = sum(history) / len(history)
    factor = 1.3

    return {
        "forecast_value": round(avg * factor, 2),
        "messages": [f"FORECAST: {avg:.2f} → adjusted"]
    }


def executive_manager_node(state: AgentState):
    stock = state["inventory_level"]
    demand = state["forecast_value"]

    if demand > stock:
        decision = f"ORDER {round((demand - stock) * 1.2)}"
    else:
        decision = "HOLD"

    return {
        "final_decision": decision,
        "messages": [f"MANAGER: {decision}"]
    }