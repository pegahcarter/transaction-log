import pandas as pd
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from database import Base, hist_prices
from functions import coin_price
from datetime import datetime
import ccxt


with open('api.txt', 'r') as f:
	api = f.readlines()
	apiKey = api[0][:len(api[0])-1]
	secret = api[1][:len(api[1])]

class Portfolio(object):

	def __init__(self):

		exchange = ccxt.binance({
			'options': {'adjustForTimeDifference': True},
			'apiKey': apiKey,
			'secret': secret
		})
		balance = exchange.fetchBalance()

		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]

		quantities = [balance[coin]['total'] for coin in coins]
		current_prices = [coin_price(coin) for coin in coins]

		self.coins = coins
		self.quantities = quantities
		self.current_prices = current_prices
		self.dollar_values = quantities * current_prices


	def execute_trade(self, coin_indices, dollar_amt, current_prices):
		buy_index, sell_index = coin_indices
		# Include a 1% slippage rate and 0.1% trading fee
		self.quantities[buy_index] += (dollar_amt / current_prices[buy_index] * 0.989)
		self.quantities[sell_index] += (dollar_amt / current_prices[sell_index])













class Transaction(Base):
	__tablename__ = 'transactions'

	trade_num = Column(Integer, primary_key=True)
	date = Column(DateTime, default=datetime.utcnow)
	coin = Column(String(10), ForeignKey=True)
	side = Column(String(10))
	units = Column(Float(10,2))
	price_per_unit = Column(Float(10,2))
	fees = Column(Float(10,2))
	previous_units = Column(Float(10,2))
	cumulative_units = Column(Float(10,2))
	transacted_value = Column(Float(10,2))
	previous_cost = Column(Float(10,2))
	cost_of_transaction = Column(Float(10,2))
	cost_per_unit = Column(Float(10,2))
	cumulative_cost = Column(Float(10,2))
	gain_loss = Column(Float(10,2))
	realised_pct = Column(Float(10,2))

	def __init__(
		self,
		trade_num=None,
		date=None,
		coin=None,
		side=None,
		units=None,
		price_per_unit=None,
		fees=None,
		previous_units=None,
		cumulative_units=None,
		transacted_value=None,
		previous_cost=None,
		cost_of_transaction=None,
		cost_per_unit=None,
		cumulative_cost=None,
		gain_loss=None,
		realised_pct=None):

		self.trade_num = trade_num
		self.date = date
		self.coin = coin
		self.side = side
		self.units = units
		self.price_per_unit = price_per_unit
		self.fees = fees
		self.previous_units = previous_units
		self.cumulative_units = cumulative_units
		self.transacted_value = transacted_value
		self.previous_cost = previous_cost
		self.cost_of_transaction = cost_of_transaction
		self.cost_per_unit = cost_per_unit
		self.cumulative_cost = cumulative_cost
		self.gain_loss = gain_loss
		self.realised_pct = realised_pct
