import numpy as np
import pandas as pd
import exchange
import ccxt

class Portfolio(object):
	'''
	Represents our account balance on Binance
	coins	- list of coin names we are invested in
	units	- list of the units for each coin held
	prices 	- list of the most recent dollar price for each coin held
	d_vals  - list of the dollar values for each coin held (units * prices)
	'''
	def __init__(self):
		api = pd.read_csv('../api.csv')
		binance = ccxt.binance({'options': {'adjustForTimeDifference': True},
								 'apiKey': api['apiKey'],
								 'secret': api['secret']})

		balance = binance.fetchBalance()
		coins =	[asset['asset']
				 for asset in balance['info']['balances']
				 if (float(asset['free']) > 0.01)]

		units = np.array([balance[coin]['total'] for coin in coins])
		prices = [exchange.fetch_price(coin, binance) for coin in coins]
		self.coins = coins
		self.units = units
		self.prices = prices
		self.d_vals = units * prices

	def create_order(param=None):
		print('success')



class Foo(object):
	def __init__(self):
		self.x = 1

	def create_order(param=None):
		if param is None:
			return 'empty'
		else:
			return param

bar = Foo()
bar.create_order('hello')
