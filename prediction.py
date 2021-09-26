from datetime import datetime
import streamlit as st
from helper import get_data


class PredictionPage:
    def __init__(self):
        pass

    def get_position_form(self):
        with st.sidebar.form(key="Ativo"):
            st.header("Escolha um ativo para analisar o comportamento futuro")
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
            cagr_revenue = st.number_input("Estimativa do CAGR da receita em %")
            cagr_carbon = st.number_input("Estimativa do CAGR do custo de carbono em %")
            carbon_intesity = st.number_input(
                "Estimativa da intensidade de carbono em tCO2e/R$", min_value=0
            )
            posicao_submit_button = st.form_submit_button(label="Analisar")

        return (
            company,
            date,
            number_of_shares,
            posicao_submit_button,
            cagr_revenue,
            cagr_carbon,
            carbon_intesity,
        )

    @staticmethod
    def get_companies_ticker() -> list:
        return get_data()["ticker"].sort_values().unique().tolist()


def app():

    prediction_page = PredictionPage()

    prediction_page.get_position_form()
