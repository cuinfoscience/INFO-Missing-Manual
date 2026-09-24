"""Weekly sales: total units and revenue per store."""

from pathlib import Path

import pandas as pd

DATA = Path("data/raw/sales.csv")


def main():
    # Read the raw export.
    df = pd.read_csv(DATA)
    df["revenue"] = df["units"] * df["price"]
    totals = df.groupby("store")[["units", "revenue"]].sum()
    print(totals)


if __name__ == "__main__":
    main()
