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
		else:
			btc_ratio = float(api.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
			return btc_ratio * btc_price


def trade(d_amt, portfolio, date=None):
	''' Execute trade on exchange to rebalance, and document said trade to transactions	'''

	# `l` == "lowest weight in portfolio", `h` == "highest weight in portfolio"
	l_coin = portfolio.coins[portfolio.d_vals.argmin()]
	h_coin= portfolio.coins[portfolio.d_vals.argmax()]
	print('Value of trade: ${}'.format(round(d_amt,2)))
	print('Sell: {}'.format(h_coin))
	print('Buy: {}\n'.format(l_coin))

	# See if ticker exists on exchange - TODO: obviously the ticker will already exist
	# 	because the pair will already exist on the DEX
	# `t` == `ticker`
	t1 = l_coin + '/' + h_coin
	t2 = h_coin + '/' + l_coin

	#	NOTE: what do we do if the pair _does not_ exist on the DEX?
	if t1 and t2 not in all_tickers:
		tickers_to_trade = [[h_coin + '/BTC'], [l_coin + '/BTC']]
		print('Coin ticker does not exist on exchange.  BTC used as base pair for both coins.')
	else:
		convert_to_btc = False
		if t1 in all_tickers:
			tickers_to_trade = [t1]
		else:
			tickers_to_trade = [t2]

	for ticker in tickers_to_trade:
		trade_coins = ticker.split('/')
		trade_sides = findSides(ticker, portfolio)
		trade_units = findUnits(ticker, d_amt)
		if date is None:
			portfolio.binance.create_order(ticker, 'market', trade_sides[0], trade_units[0])

		transactions.update(trade_coins, trade_sides, trade_units, d_amt)

	return


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
