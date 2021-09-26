from functools import lru_cache
from datetime import datetime
import streamlit as st

import pandas as pd


def get_carbon_price(date: datetime, currency="brl") -> float:
    df = pd.read_csv("carbon_price.csv")

    usd_price = st.session_state["preco_carbono_historico"]

    if currency == "brl":
        return usd_price*df.set_index("year").loc[date.year, "exchange_rate"]
    return usd_price


@lru_cache()
def get_data():
    return pd.read_csv("companies_history.csv")
