import operator
import csv
from typing import Annotated, List, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


# --- 1. STATE DEFINITION ---
class AgentState(TypedDict):
    sku: str
    inventory_level: int
    historical_sales: List[int]
    market_signal: str
    forecast_value: float
    final_decision: str
    messages: Annotated[List[str], operator.add]


# --- 2. MOCK DATABASE ---
class SupplyChainDB:
    def __init__(self):
        self.data = {}

    def add_record(self, sku: str, stock: int, sales: List[int]):
        self.data[sku] = {
            "stock": stock,
            "sales": sales
        }

    def get_record(self, sku: str):
        return self.data.get(sku, {"stock": 0, "sales": [0]})


db = SupplyChainDB()


# --- 3. LLM SETUP ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)


# --- 4. AGENT NODES ---

def data_ingestion_node(state: AgentState):
    if "inventory_level" in state and "historical_sales" in state:
        return {"messages": ["INTAKE: Using provided data."]}

    sku = state.get("sku", "UNKNOWN")
    record = db.get_record(sku)

    return {
        "inventory_level": record["stock"],
        "historical_sales": record["sales"],
        "messages": [f"INTAKE: Loaded DB data for {sku}."]
    }


def market_analyst_node(state: AgentState):
    signal = "Surge in electronics demand due to festival season."
    return {
        "market_signal": signal,
        "messages": ["ANALYST: Market surge detected."]
    }


def forecasting_node(state: AgentState):
    history = state["historical_sales"]

    if not history or sum(history) == 0:
        return {
            "forecast_value": 0,
            "messages": ["FORECASTER: No valid sales data."]
        }

    avg = sum(history) / len(history)
    factor = 1.3 if "surge" in state["market_signal"].lower() else 1.05

    forecast = round(avg * factor, 2)

    return {
        "forecast_value": forecast,
        "messages": [f"FORECASTER: {avg:.2f} → {forecast}"]
    }


def executive_manager_node(state: AgentState):
    stock = state["inventory_level"]
    demand = state["forecast_value"]

    if demand > stock:
        order_qty = round((demand - stock) * 1.2)
        decision = f"ORDER: {order_qty} units"
    else:
        decision = "HOLD: Stock sufficient"

    return {
        "final_decision": decision,
        "messages": [f"MANAGER: {decision}"]
    }


# --- 5. GRAPH SETUP ---
builder = StateGraph(AgentState)

builder.add_node("ingestion", data_ingestion_node)
builder.add_node("analyst", market_analyst_node)
builder.add_node("forecaster", forecasting_node)
builder.add_node("manager", executive_manager_node)

builder.set_entry_point("ingestion")

builder.add_edge("ingestion", "analyst")
builder.add_edge("analyst", "forecaster")
builder.add_edge("forecaster", "manager")
builder.add_edge("manager", END)

supply_chain_app = builder.compile()


# --- 6. INPUT METHODS ---

def get_user_input():
    sku = input("Enter SKU: ")
    stock = int(input("Enter inventory level: "))
    sales = list(map(int, input("Enter sales (comma-separated): ").split(",")))

    return [{
        "sku": sku,
        "inventory_level": stock,
        "historical_sales": sales
    }]


def load_csv(file_path: str):
    records = []

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append({
                "sku": row["sku"],
                "inventory_level": int(row["inventory_level"]),
                "historical_sales": list(map(int, row["historical_sales"].split(",")))
            })

    return records


# --- 7. EXECUTION ENGINE ---

def run_pipeline(records):
    for record in records:
        print("\n" + "-" * 40)
        print(f"Processing SKU: {record['sku']}")

        db.add_record(
            record["sku"],
            record["inventory_level"],
            record["historical_sales"]
        )

        config = {
            "sku": record["sku"],
            "inventory_level": record["inventory_level"],
            "historical_sales": record["historical_sales"],
            "messages": []
        }

        for output in supply_chain_app.stream(config):
            for node, data in output.items():
                print(f">>> {node.upper()}: {data['messages'][-1]}")

        final = supply_chain_app.invoke(config)

        print("\nFINAL RESULT")
        print(f"SKU: {final['sku']}")
        print(f"Forecast: {final['forecast_value']}")
        print(f"Decision: {final['final_decision']}")


# --- 8. MAIN ---

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("SUPPLY CHAIN FORECAST SYSTEM")
    print("=" * 50)

    mode = input("Choose mode (1 = Manual, 2 = CSV): ")

    try:
        if mode == "1":
            records = get_user_input()
        elif mode == "2":
            path = input("Enter CSV file path: ")
            records = load_csv(path)
        else:
            raise ValueError("Invalid mode selected")

        run_pipeline(records)

    except Exception as e:
        print(f"ERROR: {e}")