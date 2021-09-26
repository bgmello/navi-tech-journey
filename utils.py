from functools import lru_cache
import altair as alt
from PIL import Image
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

@lru_cache()
def get_data():
    return pd.read_csv('companies_history.csv')

def show_logo():
    img = Image.open("assets/logo.png")
    st.image(img)


def show_wallet():
    if not st.session_state["carteira"].empty:
        st.dataframe(st.session_state["carteira"])


def calculate_carbon_credit(carbon_credit_button):
    if carbon_credit_button:
        # st.metric(label="Custo total de offset de carbono", value="R$ 100 Milhões")
        get_bps_time_series(pd.DataFrame())


def initialize_session_variables():
    if "carteira" not in st.session_state:
        st.session_state["carteira"] = pd.DataFrame({"TICKER": [], "DATA DA COMPRA": [], "NÚMERO DE AÇÕES": []})


def get_carbon_price(date: str) -> float:
    return np.random.random()*100


def get_companies_ticker() -> list:
    return get_data()["ticker"].sort_values().unique().tolist()


def add_purchase(posicao_submit_button: bool, company: str, date: datetime, n_shares: int) -> pd.DataFrame:
    if posicao_submit_button:
        st.session_state["carteira"] = pd.concat(
            [st.session_state["carteira"], pd.DataFrame({"TICKER": [company],
                                                         "DATA DA COMPRA": [date.strftime("%d/%m/%Y")],
                                                         "NÚMERO DE AÇÕES": [int(n_shares)]})]).reset_index(
            drop=True)


def get_bps_time_series(wallet: pd.DataFrame) -> None:

    tmp = pd.DataFrame({"Ano": [int(i+2010) for i in range(10)], "BPS": [np.random.random() for i in range(10)]})

    chart = (alt.Chart(tmp)
             .mark_area(line={"color": "#F1725E"},
                        color=alt.Gradient(
                            gradient="linear",
                            stops=[alt.GradientStop(color="white", offset=0),
                                   alt.GradientStop(color="#F1725E", offset=1)],
                        x1=1,
                        x2=1,
                        y1=1,
                        y2=0
                        ),
                        point=True)
             .encode(x=alt.X("Ano", axis=alt.Axis(tickMinStep=1, labelAngle=45)), y=alt.Y("BPS:Q", axis=alt.Axis(format="%")),
                     color=alt.value("#F1725E"))
             .properties(width=700, title="Offset de carbono"))

    return st.altair_chart(chart)


def get_position_form():
    with st.form(key="Posicao"):
        st.header("Adicione Posição")
        col1, col2 = st.columns(2)
        company = st.selectbox("Escolha a empresa:", options=get_companies_ticker())
        date = col1.date_input("Data de compra:", min_value=datetime(2013, 1, 1), value=datetime.today())
        number_of_shares = col2.number_input("Número de ações", min_value=1, step=1)
        posicao_submit_button = st.form_submit_button(label="Adicione posição")

    return company, date, number_of_shares, posicao_submit_button
