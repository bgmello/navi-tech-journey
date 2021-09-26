from functools import lru_cache
from datetime import datetime

import pandas as pd


def get_carbon_price(date: datetime) -> float:
    df = pd.read_csv("carbon_price.csv")
    return df.set_index("year").loc[date.year].iloc[0]


@lru_cache()
def get_data():
    return pd.read_csv("companies_history.csv")
