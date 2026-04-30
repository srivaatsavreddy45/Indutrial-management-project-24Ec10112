import operator
from typing import Annotated, List, TypedDict
from pydantic import BaseModel


class AgentState(TypedDict):
    sku: str
    inventory_level: int
    historical_sales: List[int]
    market_signal: str
    forecast_value: float
    final_decision: str
    messages: Annotated[List[str], operator.add]


class InputSchema(BaseModel):
    sku: str
    inventory_level: int
    historical_sales: List[int]


class BatchInput(BaseModel):
    records: List[InputSchema]