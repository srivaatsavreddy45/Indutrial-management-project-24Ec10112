import pandas as pd


def load_csv(file):
    df = pd.read_csv(file)

    df["historical_sales"] = df["historical_sales"].apply(
        lambda x: list(map(int, x.split(",")))
    )

    return df.to_dict(orient="records")