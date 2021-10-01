from datetime import datetime

import pandas as pd

from helper import get_carbon_price, get_data


class Company:
    def __init__(self, ticker: str):

        self.ticker = ticker

    def get_price_by_share(self, date: datetime) -> float:
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
            return 0

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
            return (
                1000000
                * data.loc[
                    data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                    "total_revenues",
                ].iloc[0]
            )
        except IndexError:
            return None

    def get_ebt(self, date: datetime) -> float:
        data = get_data()

        try:
            return (
                1000000
                * data.loc[
                    data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                    "EBT",
                ].iloc[0]
            )
        except IndexError:
            return None

    def get_ebitda(self, date: datetime) -> float:
        data = get_data()

        try:
            return (
                1000000
                * data.loc[
                    data["ticker"].eq(self.ticker) & data["fiscal_year"].eq(date.year),
                    "EBITDA",
                ].iloc[0]
            )
        except IndexError:
            return None

    def get_carbon_offset(self, date: datetime) -> float:
        if pd.isna(self.get_total_emission(date)):
            return 0

        return get_carbon_price(date) * self.get_total_emission(date)

    def get_carbon_offset_by_price(self, date: datetime) -> float:
        if pd.isna(self.get_price_by_share(date)):
            return 0
        return (
            10000
            * self.get_carbon_offset(date)
            / (self.get_price_by_share(date) * self.get_number_of_shares(date))
        )

    def get_carbon_offset_by_ebitda(self, date: datetime) -> float:

        if pd.isna(self.get_ebitda(date)) or self.get_ebitda(date) == 0:
            return 0

        return 10000 * (self.get_carbon_offset(date)) / self.get_ebitda(date)

    def get_carbon_offset_by_ebt(self, date: datetime) -> float:

        if pd.isna(self.get_ebt(date)) or self.get_ebt(date) == 0:
            return 0

        return 10000 * (self.get_carbon_offset(date)) / self.get_ebt(date)

    def get_intensity_of_carbon_consumption(self, date: datetime) -> float:
        if self.get_net_revenue(date) == 0 or pd.isna(self.get_net_revenue(date)):
            return 0
        return self.get_total_emission(date) / self.get_net_revenue(date)


class CompanyShare:
    def __init__(self, ticker, n_shares, start_date):

        self.n_shares = n_shares
        self.company = Company(ticker)
        self.start_date = start_date

    def get_share_on_company(self, date: datetime) -> float:
        if date.year < self.start_date.year or pd.isna(
            self.company.get_number_of_shares(date)
        ):
            return 0

        return self.n_shares / self.company.get_number_of_shares(date)

    def get_price(self, date: datetime) -> float:
        if date.year < self.start_date.year or pd.isna(
            self.company.get_price_by_share(date)
        ):
            return 0

        return self.company.get_price_by_share(date) * self.n_shares

    def get_share_on_emission(self, date: datetime) -> float:
        return self.company.get_total_emission(date) * self.get_share_on_company(date)

    def get_share_on_revenue(self, date: datetime) -> float:
        if pd.isna(self.company.get_net_revenue(date)):
            return 0
        return self.company.get_net_revenue(date) * self.get_share_on_company(date)

    def get_share_on_ebitda(self, date: datetime) -> float:
        if pd.isna(self.company.get_ebitda(date)) or pd.isna(
            self.get_share_on_company(date)
        ):
            return 0
        return self.company.get_ebitda(date) * self.get_share_on_company(date)

    def get_share_on_ebt(self, date: datetime) -> float:
        if pd.isna(self.company.get_ebt(date)) or pd.isna(
            self.get_share_on_company(date)
        ):
            return 0
        return self.company.get_ebt(date) * self.get_share_on_company(date)

    def get_share_on_carbon_offset(self, date: datetime) -> float:
        if date.year == 2019:
            print(self.company.ticker)
            print(self.company.get_carbon_offset(date))
            print(self.get_share_on_company(date))
            print(self.company.get_carbon_offset(date) * self.get_share_on_company(date))

        return self.company.get_carbon_offset(date) * self.get_share_on_company(date)


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

    def get_price(self, date: datetime) -> float:
        return sum(map(lambda x: x.get_price(date), self.companies_shares))

    def get_carbon_offset(self, date: datetime) -> float:
        total_value = self.get_price(date)

        return sum(
            map(
                lambda x: (
                    x.get_share_on_carbon_offset(date) * x.get_price(date) / total_value
                    if (
                        not pd.isna(x.get_price(date))
                        and total_value != 0
                    )
                    else 0
                ),
                self.companies_shares,
            ),
            0,
        )

    def get_emission(self, date: datetime) -> float:
        total_value = self.get_price(date)

        return sum(
            map(
                lambda x: (
                    x.get_share_on_emission(date) * x.get_price(date) / total_value
                    if not pd.isna(x.get_price(date)) and total_value != 0
                    else 0
                ),
                self.companies_shares,
            ),
            0,
        )

    def get_revenue(self, date: datetime) -> float:
        total_value = self.get_price(date)

        return sum(
            map(
                lambda x: (
                    x.get_share_on_revenue(date) * x.get_price(date) / total_value
                    if not pd.isna(x.get_price(date)) and total_value != 0
                    else 0
                ),
                self.companies_shares,
            ),
            0,
        )

    def get_ebitda(self, date: datetime) -> float:
        total_value = self.get_price(date)

        return sum(
            map(
                lambda x: (
                    x.get_share_on_ebitda(date) * x.get_price(date) / total_value
                    if (
                        not pd.isna(x.get_price(date))
                        and total_value != 0
                        and not pd.isna(x.get_share_on_ebitda(date))
                    )
                    else 0
                ),
                self.companies_shares,
            ),
            0,
        )

    def get_ebt(self, date: datetime) -> float:
        total_value = self.get_price(date)

        return sum(
            map(
                lambda x: (
                    x.get_share_on_ebt(date) * x.get_price(date) / total_value
                    if not pd.isna(x.get_price(date)) and total_value != 0
                    else 0
                ),
                self.companies_shares,
            ),
            0,
        )

    def get_intesity_of_carbon_consumption(self, date: datetime) -> float:
        revenue = self.get_revenue(date)

        return self.get_emission(date) / revenue if revenue != 0 else 0

    def get_carbon_offset_by_price(self, date: datetime) -> float:
        if self.get_price(date) == 0:
            return 0

        total_value = self.get_price(date)

        return sum(map(lambda x: (x.company.get_carbon_offset_by_price(date)*x.get_price(date)/total_value), self.companies_shares))
        #return self.get_carbon_offset(date) / self.get_price(date)

    def get_carbon_offset_by_ebitda(self, date: datetime) -> float:
        if self.get_ebitda(date) == 0:
            return 0
        return self.get_carbon_offset(date) / self.get_ebitda(date)

    def get_carbon_offset_by_ebt(self, date: datetime) -> float:
        if self.get_ebt(date) == 0:
            return 0
        return self.get_carbon_offset(date) / self.get_ebt(date)
