import datetime
import numpy as np
import pandas as pd
import exchange

myPortfolio = Portfolio()
myPortfolio.coins


class Portfolio(object):
	'''
	Represents our account balance on Binance

	coins		    - list of coin names we are invested in
	units			- list of the units for each coin held
	currentPrices 	- list of the most recent dollar price for each coin held
	dollarValues  	- list of the dollar values for each coin held (units * currentPrices)

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
		currentPrices = [exchange.price(coin) for coin in coins]

		self.coins = coins
		self.units = units
		self.currentPrices = currentPrices
		self.dollarValues = units * currentPrices
		# self.cost = []
		# self.cost_per_unit = []
		# self.unrealised_amt = []
		# self.unrealised_pct = []
		# self.realised_amt = []
		# self.gain_loss = []


# TODO: add column into simulations CSV for coin price at time of trade
class SimPortfolio(object):

	def __init__(self, coins):
		self.coins = coins
		histPrices = pd.read_csv('../data/historical/prices.csv')
		self.units = [1000 / histPrices[coin][0] for coin in coins]



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
			currentPrice = exchange.price(coin)
			setattr(self, coin, {
				'units': units,
				'currentPrice': currentPrice,
				'dollarValue': units * currentPrice
			})



# ------------------------------------------------------------------------------
