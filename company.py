import numpy as np
from utils import get_carbon_price
from datetime import datetime


class Company:
    def __init__(self, ticker: str):

        self.ticker = ticker

    def get_price(self, date: datetime) -> float:
        return np.random.random()*200

    def get_total_emission(self, date: datetime) -> float:
        return np.random.random()*100

    def get_number_of_shares(self, date: datetime) -> int:
        return np.random.randint(2000)

    def get_net_revenue(self, date: datetime) -> float:
        return np.random.random()*2000

    def get_carbon_offset_by_share(self, date: datetime) -> float:
        return get_carbon_price(date)*self.get_total_emission(date)/self.get_number_of_shares(date)

    def get_bps_carbon_offset(self, date: datetime) -> float:
        return self.get_carbon_offset_by_share(date)/self.get_price(date)

    def intensity_of_carbon_consumption(self, date: datetime) -> float:
        return self.get_total_emission(date)/self.get_net_revenue(date)


class CompanyShare:
    def __init__(self, ticker, n_shares):

        self.n_shares = n_shares
        self.ticker = ticker

    def get_share_of_total_carbon_offset(self, date: datetime) -> float:
        return self.get_carbon_offset_by_share(date)*self.n_shares
