import datetime
import numpy as np
import pandas as pd
import exchange


class Portfolio(object):
	'''
	Represents our account balance on Binance

	coins		    - list of coin names we are invested in
	units			- list of the units for each coin held
	current_prices  - list of the most recent dollar price for each coin held
	dollar_values   - list of the dollar values for each coin held (units * current_prices)

	'''
	def __init__(self):

		binance = exchange.connect()
		balance = binance.fetchBalance()

		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]

		units = np.array([balance[coin]['total'] for coin in coins])
		current_prices = [exchange.price(coin) for coin in coins]

		self.coins = coins
		self.units = units
		self.current_prices = current_prices
		self.dollar_values = units * current_prices
		self.cost = []
		self.cost_per_unit = []
		self.unrealised_amt = []
		self.unrealised_pct = []
		self.realised_amt = []
		self.gain_loss = []


# TODO: add column into simulations CSV for coin price at time of trade
class SimPortfolio(object):

	def __init__(self, coins):
		self.coins = coins
		hist_prices = pd.read_csv('../data/historical/prices.csv')
		self.units = [1000 / hist_prices[coin][0] for coin in coins]



# ------------------------------------------------------------------------------
# Testing w/ using Portfolio in a JSON-like structure

class NewPortfolio(object):

	binance = exchange.connect()
	balance = binance.fetchBalance()

	def __init__(self):
		# TODO: convert code before to map() for practice
		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]
		# TODO: can the for loop be replicated with map() ?
		for coin in coins:
			# print(coin)
			# print(balance[coin]['free'])
			units = float(balance[coin]['free'])
			current_price = exchange.price(coin)
			setattr(self, coin, {
				'units': units,
				'current_price': current_price,
				'dollar_value': units * current_price
			})



# ------------------------------------------------------------------------------
