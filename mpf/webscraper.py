from datetime import datetime

import requests
from bs4 import BeautifulSoup
import json


class Fund:
    def __init__(
            self,
            scheme: str,
            name: str,
            fund_type: str,
            launch_date: datetime,
            size: float,
            risk_class: int,
            latest_fer: float,
            annual_returns: dict[str, float]
    ):
        self.scheme = scheme
        self.name = name
        self.fund_type = fund_type
        self.launch_date = launch_date
        self.size = size
        self.risk_class = risk_class
        self.latest_fer = latest_fer
        self.annual_returns = annual_returns

    def to_json(self):
        return {
            'Scheme': self.scheme,
            'Name': self.name,
            'Fund_type': self.fund_type,
            'Launch Date': self.launch_date.isoformat(),
            'Size': self.size,
            'Risk Class': self.risk_class,
            'Latest FER': self.latest_fer,
            'Annual Returns': self.annual_returns
        }


class Crawler:
    def __init__(self, start_url: str, output_path: str):
        self.start_url = start_url
        self.output_path = output_path
        self.funds: list[Fund] = []

    @staticmethod
    def fetch_site(site_url: str) -> str:
        result = requests.get(site_url)
        data = result.text
        return data

    @staticmethod
    def convert_number(data, func):
        try:
            return func(data.replace(',', ''))
        except ValueError:
            return None

    def run(self):
        html = self.fetch_site(self.start_url)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all("tr", {"class": "wr"})
        for row in rows:
            cells = row.find_all('td')
            fund = Fund(
                cells[1].text,
                cells[3].text,
                cells[5].text,
                datetime.strptime(cells[6].text, '%d-%m-%Y'),
                self.convert_number(cells[7].text, float),
                self.convert_number(cells[8].text, int),
                self.convert_number(cells[9].text, float),
                {
                    '1 Year': self.convert_number(cells[10].text, float),
                    '5 Year': self.convert_number(cells[11].text, float),
                    '10 Year': self.convert_number(cells[12].text, float)
                }
            )
            self.funds.append(fund)

        with open(self.output_path, 'w') as file:
            file.write(json.dumps([fund.to_json() for fund in self.funds]))


if __name__ == '__main__':
    scrape = Crawler('https://mfp.mpfa.org.hk/eng/mpp_list.jsp', '../dataset/funds.json')
    scrape.run()
