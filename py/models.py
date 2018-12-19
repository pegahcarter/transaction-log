import numpy as np
from functions import *
import datetime

class Portfolio(object):
	'''
	Represents our account balance on Binance

	coins           - list of coin names we are invested in
	quantities      - list of the quantities for each coin held
	current_prices  - list of the most recent dollar price for each coin held
	dollar_values   - list of the dollar values for each coin held (quantities * current_prices)

	'''
	def __init__(self):

		exchange = connect_to_exchange()
		balance = exchange.fetchBalance()

		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]

		quantities = np.array([balance[coin]['total'] for coin in coins])
		current_prices = [coin_price(coin) for coin in coins]

		self.coins = coins
		self.quantities = quantities
		self.current_prices = current_prices
		self.dollar_values = quantities * current_prices
		self.cost = []
		self.cost_per_unit = []
		self.unrealised_amt = []
		self.unrealised_pct = []
		self.realised_amt = []
		self.gain_loss = []
