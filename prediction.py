import streamlit as st
from helper import get_data
from graphics import get_intensity_carbon_consumption_time_series_forcast, get_total_emission_time_series_forecast, get_carbon_offset_time_series_forecast, get_carbon_offset_by_price_time_series_forecast


class PredictionPage:
    def __init__(self):
        pass

    def get_position_form(self):
        with st.sidebar.form(key="Ativo"):
            st.header("Escolha um ativo para analisar o comportamento futuro")
            company = st.selectbox(
                "Escolha a empresa:", options=self.get_companies_ticker()
            )
            cagr_revenue = st.number_input("Estimativa do CAGR da receita em %")
            cagr_carbon = st.number_input("Estimativa do CAGR do custo de carbono em %")
            carbon_intensity = st.number_input(
                "Estimativa da intensidade de carbono em tCO2e/Milhões de R$", min_value=0
            )
            submit_button = st.form_submit_button(label="Analisar")

        return (
            company,
            submit_button,
            cagr_revenue,
            cagr_carbon,
            carbon_intensity,
        )

    @staticmethod
    def get_companies_ticker() -> list:
        data = get_data()
        return data.loc[data["fiscal_year"].eq(2020), "ticker"].sort_values().unique().tolist()

    @staticmethod
    def show_predictions(submit_button, company, cagr_revenue, cagr_carbon, carbon_intensity):
        if submit_button:
            col1, col2 = st.columns(2)
            get_intensity_carbon_consumption_time_series_forcast(
                col1, company, carbon_intensity
            )

            get_total_emission_time_series_forecast(
                col2, company, carbon_intensity, cagr_revenue/100
            )

            get_carbon_offset_by_price_time_series_forecast(
                col1, company, cagr_carbon/100, carbon_intensity, cagr_revenue/100
            )

            get_carbon_offset_time_series_forecast(
                col2, company, cagr_carbon/100
            )


def app():

    prediction_page = PredictionPage()

    company, submit_button, cagr_revenue, cagr_carbon, carbon_intensity = prediction_page.get_position_form()

    prediction_page.show_predictions(submit_button, company, cagr_revenue, cagr_carbon, carbon_intensity)
