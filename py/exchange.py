import pandas as pd
import datetime
import ccxt
from models import *
from transactions import *

def connect_to_exchange():
	''' Connect to our exchange API and fetch our account balance '''

	with open('../../api.txt', 'r') as f:
		api = f.readlines()
		apiKey = api[0][:-1]
		secret = api[1][:-1]

	exchange = ccxt.binance({
		'options': {'adjustForTimeDifference': True},
		'apiKey': apiKey,
		'secret': secret
	})
	return exchange


def coin_price(coin):
	''' Return the current dollar price of the coin in question '''

	exchange = connect_to_exchange()
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


def find_tickers(myPortfolio):
	'''
	Determine the coin pair needed to execute the trade.
	If there isn't a pair, convert to BTC first
	(i.e. XRP/OMG becomes XRP/BTC and OMG/BTC)
	'''

	exchange = connect_to_exchange()
	coin1 = myPortfolio.coins[myPortfolio.dollar_values.argmin()]
	coin2 = myPortfolio.coins[myPortfolio.dollar_values.argmax()]
	try:
		exchange.fetch_ticker(coin1 + '/' + coin2)
		return [[coin1, coin2]]
	except:
		try:
			exchange.fetch_ticker(coin2 + '/' + coin1)
			return [[coin2, coin1]]
		except:
			return [[coin1, 'BTC'], [coin2, 'BTC']]
