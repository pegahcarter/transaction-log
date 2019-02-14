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
		if coins is not None:
			hist_prices = pd.read_csv('../data/historical/prices.csv')[['timestamp'] + coins]
			prices = hist_prices[coins].iloc[0].tolist()
			amt_each = PORTFOLIO_START_VALUE / len(coins)
			units =  np.divide(amt_each, prices)
		else:
			binance = ccxt.binance({'options': {'adjustForTimeDifference': True},
			                        'apiKey': login['apiKey'],
			                        'secret': login['secret']})

			self.binance = binance
			balance = binance.fetchBalance()
			# Only rebalance the coins we hold with at least 0.01 units (accounts for coin dust)
			coins =	[asset['asset']
					 for asset in balance['info']['balances']
					 if (float(asset['free']) > 0.01)]

			units = np.array([balance[coin]['total'] for coin in coins])
			prices = [exchange.fetch_price(coin) for coin in coins]

		self.coins = coins
		self.units = units
		self.prices = prices
		self.d_vals = units * prices
