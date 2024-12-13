import requests
from bs4 import BeautifulSoup
from price_parser import Price

def fetch_price(url, selector):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    el = soup.select_one(selector)
    if not el:
        raise ValueError("Price element not found on the page.")
    price = Price.fromstring(el.text)
    return price.amount_float
