from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd

from company import Wallet
from helper import get_carbon_price


def get_carbon_offset_by_price_time_series(session, wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "BPS": [
                wallet.get_carbon_offset_by_price(datetime(year, 1, 1))
                for year in np.arange(2013, 2021)
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
        .properties(width=600, title="Percentual da carteira em offset de carbono")
    )

    return session.altair_chart(chart)


def get_carbon_offset_time_series(session, wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "R$": [
                wallet.get_carbon_offset(datetime(year, 1, 1))
                for year in np.arange(2013, 2021)
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
        .properties(width=600, title="Custo do offset de carbono por ano")
    )

    return session.altair_chart(chart)


def get_intensity_carbon_consumption_time_series(
    session, wallet_df: pd.DataFrame
) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "tCO2e/R$": [
                wallet.get_intesity_of_carbon_consumption(datetime(year, 1, 1))
                for year in np.arange(2013, 2021)
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
        .properties(width=600, title="Intensidade de consumo de carbono por ano")
    )

    return session.altair_chart(chart)


def get_price_time_series(session, wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "R$": [
                wallet.get_price(datetime(year, 1, 1)) for year in np.arange(2013, 2021)
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
        .properties(width=600, title="Soma dos valores das ações por ano")
    )

    return session.altair_chart(chart)


def get_carbon_price_time_series(session, wallet_df: pd.DataFrame) -> None:

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2022),
            "R$": [
                get_carbon_price(datetime(year, 1, 1), currency="brl") for year in np.arange(2013, 2022)
            ],
            "$": [
                get_carbon_price(datetime(year, 1, 1), currency="usd") for year in np.arange(2013, 2022)
            ],
        }
    )

    brl_line = alt.Chart(tmp).mark_line(color="white").encode(y=alt.Y("R$", axis=alt.Axis(title="Preço em BRL", titleColor="white")),
                                                              x=alt.X("Ano", axis=alt.Axis(tickMinStep=1, labelAngle=45)))
    usd_line = alt.Chart(tmp).mark_line(color="#F1725E").encode(y=alt.Y("$", axis=alt.Axis(title="Preço em USD", titleColor="#F1725E")),
                                                                x=alt.X("Ano", axis=alt.Axis(tickMinStep=1, labelAngle=45)))

    return session.altair_chart(alt.layer(brl_line, usd_line).resolve_scale(y="independent"), use_container_width=True)


def get_total_emission_time_series(session, wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "tCO2e": [
                wallet.get_emission(datetime(year, 1, 1))
                for year in np.arange(2013, 2021)
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
            y="tCO2e",
            color=alt.value("#F1725E"),
        )
        .properties(width=600, title="Total de emissão da carteira por ano")
    )

    return session.altair_chart(chart)


def get_carbon_offset_by_ebitda_time_series(session, wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "BPS": [
                wallet.get_carbon_offset_by_ebitda(datetime(year, 1, 1))
                for year in np.arange(2013, 2021)
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
        .properties(width=600, title="Custo de emissão de carbono por EBITDA")
    )

    return session.altair_chart(chart)


def get_carbon_offset_by_ebt_time_series(session, wallet_df: pd.DataFrame) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Ano": np.arange(2013, 2021),
            "BPS": [
                wallet.get_carbon_offset_by_ebt(datetime(year, 1, 1))
                for year in np.arange(2013, 2021)
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
        .properties(width=600, title="Custo de emissão de carbono por EBT")
    )

    return session.altair_chart(chart)


def get_carbon_offset_by_price_vs_carbon_offset_by_ebitda_scatter_plot(
    session, wallet_df: pd.DataFrame
) -> None:

    wallet = Wallet(wallet_df)

    tmp = pd.DataFrame(
        {
            "Custo de offset sobre preço": [
                share.company.get_carbon_offset_by_price(datetime(2020, 1, 1))
                for share in wallet.companies_shares
            ],
            "Custo de offset sobre EBITDA": [
                share.company.get_carbon_offset_by_ebitda(datetime(2020, 1, 1))
                for share in wallet.companies_shares
            ],
            "Ticker": [share.company.ticker for share in wallet.companies_shares],
        }
    )

    tmp = tmp[tmp["Custo de offset sobre EBITDA"].ne(0)]

    chart = (
        alt.Chart(tmp)
        .mark_circle(size=60)
        .encode(
            x="Custo de offset sobre preço",
            y="Custo de offset sobre EBITDA",
            color=alt.value("#F1725E"),
            tooltip="Ticker",
        )
        .interactive()
        .properties(width=1200)
    )

    return session.altair_chart(chart)
