import pandas as pd
import datetime
import ccxt
import models
import transactions

def connect():
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


def price(coin):
	''' Return the current dollar price of the coin in question '''

	binance = connect()
	btc_price = float(binance.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(binance.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


def find_sides(ticker, myPortfolio):
	'''
	Return a tuple where the tuple[0] is the side of our trade and tuple[1]
	is for documenting the other side of the trade

	ticker - the coin we are buying and the coin we are selling, combined by '/'
	'''

	numerator = ticker[:ticker.find('/')]
	if myPortfolio.coins.index(numerator) == myPortfolio.dollar_values.argmin():
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def find_units(ticker, d_amt):
	numerator, denominator = ticker.split('/')
	return d_amt/price(numerator), d_amt/price(denominator)


def find_tickers(myPortfolio):
	'''
	Determine the coin pair needed to execute the trade.
	If there isn't a pair, convert to BTC first
	(i.e. XRP/OMG becomes XRP/BTC and OMG/BTC)
	'''

	binance = connect()
	coin1 = myPortfolio.coins[myPortfolio.dollar_values.argmin()]
	coin2 = myPortfolio.coins[myPortfolio.dollar_values.argmax()]

	try:
		binance.fetch_ticker(coin1 + '/' + coin2)
		return [coin1 + '/' + coin2]
	except:
		try:
			binance.fetch_ticker(coin2 + '/' + coin1)
			return [coin2 + '/' + coin1]
		except:
			return [coin1 + '/BTC', coin2 + '/BTC']


def trade(d_amt, myPortfolio, df):
	''' Execute trade on exchange to rebalance, and document said trade to transactions	'''

	binance = connect()
	tickers = find_tickers(myPortfolio)
	for ticker in tickers:

		sides = find_sides(ticker, myPortfolio)
		units = find_units(ticker, d_amt)

		print(binance.create_order(symbol=ticker, type='market', side=sides[0], amount=units[0]))

		for coin, coin_side, coin_units in zip(ticker.split('/'), sides, units):
			df = transactions.update(coin, coin_side, coin_units, d_amt, df)

	return df
