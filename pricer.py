#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas
import urllib
import requests
from bs4 import BeautifulSoup

LIGAMAGIC_SEARCH_URL = "https://www.ligamagic.com.br/?view=cards%2Fsearch&"


def get_prices(cards):
    prices = []
    for card in cards:
        encoded_cardname = urllib.urlencode({"card": card})
        url = '{prefix}{card_name}'.format(
            prefix=LIGAMAGIC_SEARCH_URL,
            card_name=encoded_cardname
        )
        resp = requests.get(url)
        if not resp.status_code == 200:
            continue

        page = BeautifulSoup(resp.content, 'html.parser')
        lower_price = page.find('font', attrs={'class': 'bigger'})
        price = ''
        if lower_price:
            price = lower_price.text

        print('Card: {} - Price: {}'.format(card, price))
        prices.append(price)

    return prices


cards = pandas.read_csv('cards.csv')
cards_list = cards['Card'].tolist()
prices = get_prices(cards_list)
cards['Valor mínimo da Liga'] = prices
cards.to_csv('cards_priced.csv', index=False)
