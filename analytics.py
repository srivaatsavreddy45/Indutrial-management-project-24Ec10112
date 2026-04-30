import pandas as pd
import matplotlib.pyplot as plt


def load_and_prepare(file_path):
    df = pd.read_csv(file_path)

    df["historical_sales"] = df["historical_sales"].apply(
        lambda x: list(map(int, x.split(",")))
    )

    df["avg_sales"] = df["historical_sales"].apply(lambda x: sum(x) / len(x))
    df["forecast"] = df["avg_sales"] * 1.3  # same logic as your agent
    df["gap"] = df["forecast"] - df["inventory_level"]

    return df


def plot_top_demand(df):
    top = df.sort_values("forecast", ascending=False).head(10)

    plt.figure()
    plt.bar(top["sku"], top["forecast"])
    plt.title("Top 10 SKUs by Forecasted Demand")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_stock_vs_demand(df):
    sample = df.head(20)

    plt.figure()
    plt.plot(sample["sku"], sample["inventory_level"], label="Stock")
    plt.plot(sample["sku"], sample["forecast"], label="Forecast")
    plt.xticks(rotation=45)
    plt.legend()
    plt.title("Stock vs Forecast (Sample SKUs)")
    plt.tight_layout()
    plt.show()


def plot_gap_distribution(df):
    plt.figure()
    plt.hist(df["gap"], bins=30)
    plt.title("Demand-Supply Gap Distribution")
    plt.tight_layout()
    plt.show()


def generate_insights(df):
    total_skus = len(df)
    shortage = df[df["gap"] > 0]
    excess = df[df["gap"] <= 0]

    print("\n📊 INSIGHTS")
    print("=" * 40)

    print(f"Total SKUs: {total_skus}")
    print(f"Shortage SKUs: {len(shortage)}")
    print(f"Excess Stock SKUs: {len(excess)}")

    print(f"Avg Forecast: {df['forecast'].mean():.2f}")
    print(f"Max Demand SKU: {df.loc[df['forecast'].idxmax(), 'sku']}")

    print("=" * 40)