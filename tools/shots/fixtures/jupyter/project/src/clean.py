"""Cleaning steps for the sales export, imported by the notebooks."""
import pandas as pd


def load_sales(path):
    """Read the raw export and parse its dates."""
    return pd.read_csv(path, parse_dates=["date"])


def add_revenue(df):
    """Units times price, as a new column."""
    return df.assign(revenue=df["units"] * df["price"])
