import numpy as np
import pandas as pd
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from database import Base
from functions import coin_price, connect_to_exchange
import datetime
import ccxt


class Portfolio(object):
	''' Represents our account balance on Binance

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


class Transaction(Base):
	''' Represents a trade executed between two coins '''

	__tablename__ = 'transactions'

	trade_num = Column(Integer, primary_key=True)
	date = Column(DateTime, default=datetime.datetime.utcnow)
	coin = Column(String(10))
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

	# def __init__(
	# 	self,
	# 	coin=None,
	# 	side=None,
	# 	units=None,
	# 	price_per_unit=None,
	# 	cumulative_cost=None,
	# 	fees=None,
	# 	previous_units=0,
	# 	cumulative_units,
	# 	transacted_value,
	# 	previous_cost=0,
	# 	cost_of_transaction=None,
	# 	cost_per_unit=None,
	# 	gain_loss=None,
	# 	realised_pct=None):
	#
	# 	self.coin = coin
	# 	self.side = side
	# 	self.units = units
	# 	self.price_per_unit = coin_price(coin)
	# 	self.fees = price_per_unit * units * 0.00075
	# 	self.previous_units = previous_units
	# 	self.cumulative_units = cumulative_units
	# 	self.transacted_value = transacted_value
	# 	self.previous_cost = previous_cost
	# 	self.cost_of_transaction = cost_of_transaction
	# 	self.cost_per_unit = cost_per_unit
	# 	# self.cumulative_cost = coin_price(coin) * units
	# 	self.gain_loss = gain_loss
	# 	self.realised_pct = realised_pct
