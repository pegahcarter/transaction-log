import numpy as np
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from database import Base
from functions import *
import datetime
import ccxt


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


class Transaction(Base):
	''' Represents a trade executed between two coins '''

	__tablename__ = 'Transactions'

	trade_num = Column(Integer, primary_key=True)
	date = Column(DateTime, default=datetime.datetime.utcnow)
	coin = Column(String(10))
	side = Column(String(10))
	units = Column(Float(10,2))
	price_per_unit = Column(Float(10,2))
	fees = Column(Float(10,2), nullable=True)
	previous_units = Column(Float(10,2), server_default='0')
	cumulative_units = Column(Float(10,2))
	transacted_value = Column(Float(10,2))
	previous_cost = Column(Float(10,2), nullable=True)
	cost_of_transaction = Column(Float(10,2), nullable=True)
	cost_per_unit = Column(Float(10,2), nullable=True)
	cumulative_cost = Column(Float(10,2), nullable=True)
	gain_loss = Column(Float(10,2), nullable=True)
	realised_pct = Column(Float(10,2), nullable=True)
