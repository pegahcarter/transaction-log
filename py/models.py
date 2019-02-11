import numpy as np
import pandas as pd
import exchange
import ccxt

# TODO: add column into simulations CSV for coin price at time of trade
class Portfolio(object):
	'''
	Represents our account balance on Binance
	coins	- list of coin names we are invested in
	units	- list of the units for each coin held
	prices 	- list of the most recent dollar price for each coin held
	d_vals  - list of the dollar values for each coin held (units * prices)
	'''
	def __init__(self, coins=None, d_amt=None):
		if coins:
			hist_prices = pd.read_csv('../data/historical/prices.csv')
			prices = [hist_prices[coin][0] for coin in coins]
			units =  np.divide(prices, d_amt/len(coins))
		else:
			df = pd.read_csv('../api.csv')
			binance = ccxt.binance({'options': {'adjustForTimeDifference': True},
									'apiKey': df['apiKey'],
									'secret': df['secret']})

			balance = binance.fetchBalance()
			# Only rebalance the coins we hold with at least 0.01 units (accounts for coin dust)
			coins =	[asset['asset']
					 for asset in balance['info']['balances']
					 if (float(asset['free']) > 0.01)]

			units = np.array([balance[coin]['total'] for coin in coins])
			prices = [exchange.fetch_price(coin) for coin in coins]
			self.binance = binance

		self.coins = coins
		self.units = units
		self.prices = prices
		self.d_vals = units * prices
