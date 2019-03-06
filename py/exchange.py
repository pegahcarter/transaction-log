import ccxt
import pandas as pd
import transactions

api = ccxt.binance()
all_tickers = list(api.fetch_tickers().keys())


def fetch_price(coin, date=None):
	''' Return the current dollar price of the coin in question '''

	if date:
		pass # TODO: add @param for simulation
	else:
		# No date means we're executing the trade in real time
		btc_price = float(api.fetch_ticker('BTC/USDT')['info']['lastPrice'])
		if coin == 'BTC':
			return btc_price
		elif coin == 'USDT':
			return 1.0
		else:
			btc_ratio = float(api.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
			return btc_ratio * btc_price


def trade(d_amt, portfolio, date=None):
	''' Execute trade on exchange to rebalance, and document said trade to transactions	'''

	tickers = find_tickers(portfolio)
	print(tickers)

	for ticker in tickers:
		trade_coins = ticker.split('/')
		trade_sides = findSides(ticker, portfolio)
		trade_units = findUnits(ticker, d_amt)
		if date is None:
			portfolio.binance.create_order(ticker, 'market', trade_sides[0], trade_units[0])

		transactions.update(trade_coins, trade_sides, trade_units, d_amt)


	return


def find_tickers(portfolio):
	'''
	Determine the coin pair needed to execute the trade.
	If there isn't a pair, convert to BTC first
	(i.e. XRP/OMG becomes XRP/BTC and OMG/BTC)
	'''

	coin1 = portfolio.coins[portfolio.d_vals.argmin()]
	coin2 = portfolio.coins[portfolio.d_vals.argmax()]
	if coin1 + '/' + coin2 in all_tickers:
		return [coin1 + '/' + coin2]
	elif coin2 + '/' + coin1 in all_tickers:
		return [coin2 + '/' + coin1]
	else:
		return [coin2 + '/BTC', coin1 + '/BTC']


def findSides(ticker, portfolio):
	'''
	Return a tuple where the tuple[0] is the side of our trade and tuple[1]
	is for documenting the other side of the trade
	'''

	numerator = ticker[:ticker.find('/')]
	if portfolio.coins.index(numerator) == portfolio.d_vals.argmin():
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def findUnits(ticker, d_amt, date=None): # TODO: add @param for simulation

	numerator, denominator = ticker.split('/')
	return [d_amt/fetch_price(numerator, date), d_amt/fetch_price(denominator, date)]
