from datetime import datetime

import pandas as pd
import streamlit as st
from millify import prettify
from PIL import Image

from company import Company
from graphics import (
    get_bps_time_series,
    get_carbon_offset_time_series,
    get_intensity_carbon_consumption_time_series,
)
from helper import get_data


class HomePage:
    def __init__(self):
        pass

    @staticmethod
    def show_logo():
        img = Image.open("assets/logo.png")
        st.image(img)

    @staticmethod
    def show_wallet():
        if not st.session_state["carteira"].empty:
            st.dataframe(st.session_state["carteira"])

    @staticmethod
    def initialize_session_variables():
        if "carteira" not in st.session_state:
            st.session_state["carteira"] = pd.DataFrame()

    @staticmethod
    def add_purchase(
        posicao_submit_button: bool, ticker: str, date: datetime, n_shares: int
    ) -> pd.DataFrame:
        if posicao_submit_button:
            company = Company(ticker)
            price = company.get_price(date)
            if price is None:
                st.write("Posição não pode ser adicionada por falta de dados")

            else:
                st.session_state["carteira"] = pd.concat(
                    [
                        st.session_state["carteira"],
                        pd.DataFrame(
                            {
                                "TICKER": [ticker],
                                "DATA DA COMPRA": [date.strftime("%d/%m/%Y")],
                                "NÚMERO DE AÇÕES": [int(n_shares)],
                                "PREÇO TOTAL": [
                                    f"R$ {prettify(round(price*n_shares, 2))}"
                                ],
                            }
                        ),
                    ]
                ).reset_index(drop=True)

    def get_position_form(self):
        with st.form(key="Posicao"):
            st.header("Adicione Posição")
            col1, col2 = st.columns(2)
            company = st.selectbox(
                "Escolha a empresa:", options=self.get_companies_ticker()
            )
            date = col1.date_input(
                "Data de compra:",
                min_value=datetime(2013, 1, 1),
                max_value=datetime(2020, 12, 31),
                value=datetime(2013, 1, 1),
            )
            number_of_shares = col2.number_input("Número de ações", min_value=1, step=1)
            posicao_submit_button = st.form_submit_button(label="Adicione posição")

        return company, date, number_of_shares, posicao_submit_button

    @staticmethod
    def get_companies_ticker() -> list:
        return get_data()["ticker"].sort_values().unique().tolist()

    @staticmethod
    def show_metrics(metrics_button):
        if metrics_button:
            # st.metric(label="Custo total de offset de carbono", value="R$ 100 Milhões")
            get_bps_time_series(st.session_state["carteira"])
            get_carbon_offset_time_series(st.session_state["carteira"])
            get_intensity_carbon_consumption_time_series(st.session_state["carteira"])
