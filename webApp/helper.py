from datetime import datetime
from functools import lru_cache

import pandas as pd
import streamlit as st


def get_carbon_price(date: datetime, currency="brl") -> float:
    df = pd.read_csv("exchange_rate.csv")

    usd_price = st.session_state["preco_carbono_historico"]

    if currency == "brl":
        return usd_price * df.set_index("year").loc[date.year, "exchange_rate"]
    return usd_price


@lru_cache()
def get_data():
    return pd.read_csv("companies_history.csv")
