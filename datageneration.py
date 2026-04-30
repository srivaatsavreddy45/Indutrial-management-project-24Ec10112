import csv
import random
import os
import math


def generate_realistic_data(filename="data/big_data.csv", rows=5000):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "inventory_level", "historical_sales"])

        for i in range(rows):
            sku = f"ELEC{i:05d}"

            base = random.randint(10, 40)

            sales = []
            for t in range(12):
                trend = base + t * random.uniform(0.5, 1.5)
                season = 5 * math.sin(2 * math.pi * t / 12)
                noise = random.uniform(-3, 3)

                value = max(1, int(trend + season + noise))
                sales.append(value)

            stock = random.randint(20, 200)

            writer.writerow([sku, stock, ",".join(map(str, sales))])

    print(f"Generated {rows} realistic rows")


generate_realistic_data()