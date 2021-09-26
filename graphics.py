from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from company import Wallet


def get_bps_time_series(wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2020),
            "BPS": [
                wallet.get_bps_carbon_offset(datetime(year, 1, 1))
                for year in np.arange(2013, 2020)
            ],
        }
    )

    chart = (
        alt.Chart(tmp)
        .mark_area(
            line={"color": "#F1725E"},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="white", offset=0),
                    alt.GradientStop(color="#F1725E", offset=1),
                ],
                x1=1,
                x2=1,
                y1=1,
                y2=0,
            ),
            point=True,
        )
        .encode(
            x=alt.X("Ano", axis=alt.Axis(tickMinStep=1, labelAngle=45)),
            y="BPS",
            color=alt.value("#F1725E"),
        )
        .properties(width=700, title="Percentual da carteira em offset de carbono")
    )

    return st.altair_chart(chart)


def get_carbon_offset_time_series(wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2020),
            "R$": [
                wallet.get_total_carbon_offset(datetime(year, 1, 1))
                for year in np.arange(2013, 2020)
            ],
        }
    )

    chart = (
        alt.Chart(tmp)
        .mark_area(
            line={"color": "#F1725E"},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="white", offset=0),
                    alt.GradientStop(color="#F1725E", offset=1),
                ],
                x1=1,
                x2=1,
                y1=1,
                y2=0,
            ),
            point=True,
        )
        .encode(
            x=alt.X("Ano", axis=alt.Axis(tickMinStep=1, labelAngle=45)),
            y="R$",
            color=alt.value("#F1725E"),
        )
        .properties(width=700, title="Custo do offset de carbono por ano")
    )

    return st.altair_chart(chart)


def get_intensity_carbon_consumption_time_series(wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2020),
            "tCO2e/R$": [
                wallet.get_intesity_of_carbon_consumption(datetime(year, 1, 1))
                for year in np.arange(2013, 2020)
            ],
        }
    )

    chart = (
        alt.Chart(tmp)
        .mark_area(
            line={"color": "#F1725E"},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="white", offset=0),
                    alt.GradientStop(color="#F1725E", offset=1),
                ],
                x1=1,
                x2=1,
                y1=1,
                y2=0,
            ),
            point=True,
        )
        .encode(
            x=alt.X("Ano", axis=alt.Axis(tickMinStep=1, labelAngle=45)),
            y="tCO2e/R$",
            color=alt.value("#F1725E"),
        )
        .properties(width=700, title="Intensidade de consumo de carbono por ano")
    )

    return st.altair_chart(chart)
