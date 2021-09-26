from datetime import datetime

import pandas as pd

from helper import get_carbon_price, get_data


class Company:
    def __init__(self, ticker: str):

        self.ticker = ticker

    def get_price(self, date: datetime) -> float:
        data = get_data()

        try:
            return data.loc[
                data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                "average_price",
            ].iloc[0]
        except IndexError:
            return None

    def get_total_emission(self, date: datetime) -> float:
        data = get_data()

        try:
            return data.loc[
                data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                "emissions",
            ].iloc[0]
        except IndexError:
            return None

    def get_number_of_shares(self, date: datetime) -> int:
        data = get_data()

        try:
            return data.loc[
                data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                "out_shares",
            ].iloc[0]
        except IndexError:
            return None

    def get_net_revenue(self, date: datetime) -> float:
        data = get_data()

        try:
            return data.loc[
                data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                "total_revenue",
            ].iloc[0]
        except IndexError:
            return None

    def get_carbon_offset_by_share(self, date: datetime) -> float:
        return (
            get_carbon_price(date)
            * self.get_total_emission(date)
            / self.get_number_of_shares(date)
        )

    def get_bps_carbon_offset(self, date: datetime) -> float:
        return 10000 * self.get_carbon_offset_by_share(date) / self.get_price(date)


class CompanyShare:
    def __init__(self, ticker, n_shares, start_date):

        self.n_shares = n_shares
        self.company = Company(ticker)
        self.start_date = start_date

    def get_share_on_emission(self, date: datetime) -> float:
        if date < self.start_date:
            return 0

        return (
            self.company.get_total_emission(date)
            * self.n_shares
            / self.company.get_number_of_shares(date)
        )

    def get_share_on_revenue(self, date: datetime) -> float:
        if date < self.start_date:
            return 0

        return (
            self.company.get_net_revenue(date)
            * self.n_shares
            / self.company.get_number_of_shares(date)
        )

    def get_price(self, date: datetime) -> float:
        return self.company.get_price(date)

    def get_bps_carbon_offset(self, date: datetime) -> float:
        if date < self.start_date:
            return 0
        return self.company.get_bps_carbon_offset(date)

    def get_total_carbon_offset(self, date: datetime) -> float:
        if date < self.start_date:
            return 0
        return self.company.get_carbon_offset_by_share(date) * self.n_shares


class Wallet:
    def __init__(self, df: pd.DataFrame):

        self.companies_shares = []

        for _, position in df.iterrows():
            self.companies_shares.append(
                CompanyShare(
                    position["TICKER"],
                    position["NÚMERO DE AÇÕES"],
                    pd.to_datetime(position["DATA DA COMPRA"]),
                )
            )

    def get_bps_carbon_offset(self, date: datetime) -> float:
        total_value = sum(
            filter(
                lambda x: x is not None,
                map(lambda x: x.get_price(date), self.companies_shares),
            ),
            0,
        )

        return sum(
            map(
                lambda x: (
                    x.get_bps_carbon_offset(date) * x.get_price(date) / total_value
                    if x.get_price(date) is not None
                    else 0
                ),
                self.companies_shares,
            ),
            0,
        )

    def get_total_carbon_offset(self, date: datetime) -> float:
        return sum(
            map(lambda x: x.get_total_carbon_offset(date), self.companies_shares)
        )

    def get_intesity_of_carbon_consumption(self, date: datetime) -> float:
        revenue = sum(
            map(lambda x: x.get_share_on_revenue(date), self.companies_shares)
        )

        if revenue == 0:
            return 0

        return sum(
            map(lambda x: x.get_share_on_emission(date), self.companies_shares)
        ) / sum(map(lambda x: x.get_share_on_revenue(date), self.companies_shares))
