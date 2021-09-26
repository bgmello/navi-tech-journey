from functools import lru_cache

import pandas as pd


def get_carbon_price(date: str) -> float:
    df = pd.read_csv("carbon_price.csv")
    return df.set_index("year").loc[date.year, "price"]


@lru_cache()
def get_data():
    return pd.read_csv("companies_history.csv")
