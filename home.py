from datetime import datetime

import pandas as pd
import streamlit as st
from millify import prettify

from company import Company
from graphics import (
    get_carbon_offset_by_price_time_series,
    get_carbon_offset_time_series,
    get_carbon_price_time_series,
    get_intensity_carbon_consumption_time_series,
    get_price_time_series,
    get_total_emission_time_series,
    get_carbon_offset_by_ebitda_time_series,
    get_carbon_offset_by_ebt_time_series,
    get_carbon_offset_by_price_vs_carbon_offset_by_ebitda_scatter_plot,
)
from helper import get_data


class HomePage:
    def __init__(self):
        pass

    @staticmethod
    def show_wallet():
        if not st.session_state["carteira"].empty:
            st.write("Resumo da carteira")
            st.dataframe(st.session_state["carteira"])

        else:
            st.write("Adicione uma posição na sua carteira")

    @staticmethod
    def show_metrics(metrics_button):
        if metrics_button:
            with st.expander("Métricas de carbono"):
                col1, col2 = st.columns(2)
                get_carbon_offset_by_price_time_series(
                    col1, st.session_state["carteira"]
                )
                get_carbon_offset_time_series(col2, st.session_state["carteira"])
                get_carbon_price_time_series(col1, st.session_state["carteira"])
                get_total_emission_time_series(col2, st.session_state["carteira"])
            with st.expander("Métricas operacionais"):
                col1, col2 = st.columns(2)
                get_intensity_carbon_consumption_time_series(
                    col1, st.session_state["carteira"]
                )
                get_price_time_series(col2, st.session_state["carteira"])
                get_carbon_offset_by_ebitda_time_series(
                    col1, st.session_state["carteira"]
                )
                get_carbon_offset_by_ebt_time_series(col2, st.session_state["carteira"])
                get_carbon_offset_by_price_vs_carbon_offset_by_ebitda_scatter_plot(
                    st, st.session_state["carteira"]
                )

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
            price = company.get_price_by_share(date)
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
        with st.sidebar.form(key="Posicao"):
            st.header("Adicione Posição")
            company = st.selectbox(
                "Escolha a empresa:", options=self.get_companies_ticker()
            )
            number_of_shares = st.number_input("Número de ações", min_value=1, step=1)
            date = st.date_input(
                "Data de compra:",
                min_value=datetime(2013, 1, 1),
                max_value=datetime(2020, 12, 31),
                value=datetime(2013, 1, 1),
            )
            posicao_submit_button = st.form_submit_button(label="Adicione posição")

        return company, date, number_of_shares, posicao_submit_button

    @staticmethod
    def get_companies_ticker() -> list:
        return get_data()["ticker"].sort_values().unique().tolist()


def app():
    # Instancia classe da pagina home
    home_page = HomePage()

    # Inicializa variaveis da sessao
    home_page.initialize_session_variables()

    # Pega informacoes de posicao da carteira a partir do form
    (
        company,
        date,
        number_of_shares,
        posicao_submit_button,
    ) = home_page.get_position_form()

    # Adiciona posicao na carteira
    home_page.add_purchase(posicao_submit_button, company, date, number_of_shares)

    # Mostra a carteira
    home_page.show_wallet()

    # Cria botao para calcular metricas
    metrics_button = st.sidebar.button(label="Calcule métricas de carbono")

    # Mostra as metricas calculadas
    home_page.show_metrics(metrics_button)
