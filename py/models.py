import datetime
import numpy as np
import pandas as pd
import exchange

[u'BTC', u'ETH', u'BNB', u'OMG', u'BAT', u'XRP']

# test = [868.37775099, 879.54951063, 901.19302644, 888.91718454, 854.9576775, 894.77186726]
#
# avg_weight = 1.0/len(test)
#
#
# avg_weight - min(test)/sum(test)
# max(test)/sum(test)-avg_weight
#
#
# min(test)/sum(test)
#
# 
#
# max(test)
# sum(test) * avg_weight
#
#
# thresh = 0.01
#
# 2 * avg_weight * thresh
#





class Portfolio(object):
	'''
	Represents our account balance on Binance

	coins           - list of coin names we are invested in
	quantities      - list of the quantities for each coin held
	current_prices  - list of the most recent dollar price for each coin held
	dollar_values   - list of the dollar values for each coin held (quantities * current_prices)

	'''
	def __init__(self):

		binance = exchange.connect()
		balance = binance.fetchBalance()

		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]

		quantities = np.array([balance[coin]['total'] for coin in coins])
		current_prices = [exchange.price(coin) for coin in coins]

		self.coins = coins
		self.quantities = quantities
		self.current_prices = current_prices
		self.dollar_values = quantities * current_prices
		# self.cost = []
		# self.cost_per_unit = []
		# self.unrealised_amt = []
		# self.unrealised_pct = []
		# self.realised_amt = []
		# self.gain_loss = []



class SimPortfolio(object):

	def __init__(self, coins):
		self.coins = coins
		hist_prices = pd.read_csv('../data/historical/prices.csv')
		self.quantities = [1000 / hist_prices[coin][0] for coin in coins]
