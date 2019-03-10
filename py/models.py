import sys
import ccxt
import pandas as pd
import numpy as np
import exchange


class Portfolio(object):
	'''
	Represents our account balance on Binance
	coins	- list of coin names we are invested in
	units	- list of the units for each coin held
	prices 	- list of the most recent dollar price for each coin held
	d_vals  - list of the dollar values for each coin held (units * prices)
	'''

	def __init__(self, coins=None, PORTFOLIO_START_VALUE=None):
		if PORTFOLIO_START_VALUE is not None:
			hist_prices = pd.read_csv()[['timestamp'] + coins_in_portfolio]
			amt_each = PORTFOLIO_START_VALUE / len(coins_in_portfolio)
			units =  np.divide(amt_each, prices)
			prices = hist_prices[coins_in_portfolio].iloc[0]
			date = hist_prices[0]
		else:
			# This is not a simulation.  Rebalance our own portfolio.
			try:
				api = pd.read_csv('../../api.csv')
			except:
				api = pd.read_csv('../api.csv')
			self.binance = ccxt.binance({'options': {'adjustForTimeDifference': True},
			                        'apiKey': api['apiKey'][0],
			                        'secret': api['secret'][0]})

			coins_units_all = self.binance.fetchBalance()['free']
			# 1. Ignore "coin dust", i.e. the small fraction of coin that sometimes
			# 		remains if we aren't able to perfectly sell/transfer 100% of the coin
			# 2. This is based on units of coin owned: if we're rebalancing a coin
			# 		priced at $1 million/coin, units will be less than 0.01
			coins_in_portfolio = {coin: units for coin, units in coins_units_all.items() if units > 0.01 and coin != 'ENJ'}
			hist_prices = None
			coins = list(coins_in_portfolio.keys())
			units = np.array(list(coins_in_portfolio.values()))
			prices = [exchange.fetch_price(coin) for coin in coins_in_portfolio]
			date = None

		self.coins = coins
		self.hist_prices = hist_prices
		self.units = units
		self.prices = prices
		self.date = date
		self.d_vals = units * prices
