from analytics import (
    load_and_prepare,
    plot_top_demand,
    plot_stock_vs_demand,
    plot_gap_distribution,
    generate_insights,
)

FILE = "data/big_data.csv"

df = load_and_prepare(FILE)

generate_insights(df)

plot_top_demand(df)
plot_stock_vs_demand(df)
plot_gap_distribution(df)