from .graph import graph
from .db import save_result


def run_single(record):
    config = {**record, "messages": []}

    final = graph.invoke(config)

    save_result(
        record["sku"],
        record["inventory_level"],
        final["forecast_value"],
        final["final_decision"],
    )

    return final


def run_batch(records):
    return [run_single(r) for r in records]