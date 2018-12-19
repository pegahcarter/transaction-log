from sqlalchemy import create_engine
from models import Transaction
import pandas as pd
import datetime
import ccxt

def connect_to_exchange():
	# Connect to our exchange API and fetch our account balance
	with open('../../api.txt', 'r') as f:
		api = f.readlines()
		apiKey = api[0][:-1]
		secret = api[1][:-1]

	exchange = ccxt.binance({
		'options': {'adjustForTimeDifference': True},
		'apiKey': apiKey,
		'secret': secret
	})
	return exchange

def refresh_df():
	engine = create_engine('sqlite:///data/transactions.db')
	df = pd.read_sql_table('transactions', con=engine)
	return df


def coin_price(coin):
	'''Returns the current dollar price of the coin in question'''
	exchange = connect_to_exchange()
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


def find_sides(ticker, myPortfolio):
	''' Returns a tuple where the tuple[0] is the side of our trade and tuple[1]
	is for documenting the other side of the trade

	numerator 	- coin before the '/' in the ticker
	'''
	numerator = ticker[:ticker.find('/')]
	if myPortfolio.coins.index(numerator) == myPortfolio.dollar_values.argmin():
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def find_quantities(ticker, d_amt):
	numerator, denominator = ticker.split('/')
	return d_amt/coin_price(numerator), d_amt/coin_price(denominator)


def find_tickers(myPortfolio):
	'''Determines the coin pair needed to execute the trade.
	If there isn't a pair, convert to BTC first (like XRP/OMG)
	'''
	exchange = connect_to_exchange()

	coin1 = myPortfolio.coins[myPortfolio.dollar_values.argmin()]
	coin2 = myPortfolio.coins[myPortfolio.dollar_values.argmax()]

	try:
		exchange.fetch_ticker(coin1 + '/' + coin2)
		return [[coin1, coin2]]
	except:
		try:
			exchange.fetch_ticker(coin2 + '/' + coin1)
			return [[coin2, coin1]]
		except:
			return [[coin1, 'BTC'], [coin2, 'BTC']]


def execute_trade(d_amt, myPortfolio):

	exchange = connect_to_exchange()
	tickers = find_tickers(myPortfolio)

	for ticker in tickers:
		df = refresh_df()

		sides = find_sides(ticker, myPortfolio)
		quantities = find_quantities(ticker, d_amt)

		exchange.create_order(symbol=ticker, type='market', side=sides[0], amount=quantities[0])

		for coin, side, quantity in zip(tickers.split('/'), sides, quantities):
			update_transactions(coin, side, quantity, d_amt)


def add_coin_to_transactions(coin, quantity):
	current_price = coin_price(coin)
	myTransaction = Transaction(
		coin = coin,
		side = 'buy',
		units = quantity,
		fees = current_price * quantity * 0.00075,
		previous_units = 0,
		cumulative_units = quantity,
		transacted_value = current_price * quantity,
		previous_cost = 0,
		cost_of_transaction = None,
		cost_per_unit=None,
		cumulative_cost = current_price * quantity,
		gain_loss=None,
		realised_pct=None
	)

	db_session.add(myTransaction)
	db_session.commit()


def update_transactions(coin, side, quantity, dollar_value):
	'''Documents transaction data to SQL table

	coin 			- coin we're documenting for the trade
	side 			- side we're executing the trade on (buy or sell)
	quantity 		- quantity of coin to be traded
	dollar_value 	- value of our trade in dollars
	'''

	df = refresh_df()
	previous_units, previous_cost = df[df['coin'] == coin][['cumulative_units', 'cumulative_cost']].iloc[-1, :]

	if side == 'buy':
		myTransaction = Transaction(
			coin = coin,
			side = side,
			units = quantity,
			fees = dollar_value * 0.00075,
			previous_units = previous_units,
			cumulative_units = previous_units + quantity,
			transacted_value = dollar_value,
			previous_cost = previous_cost,
			cost_of_transaction=None,
			cost_per_unit=None,
			cumulative_cost = previous_cost + dollar_value,
			gain_loss=None,
			realised_pct=None
		)
	else:
		myTransaction = Transaction(
			coin = coin,
			side = side,
			units = quantity,
			fees = None,
			previous_units = previous_units,
			cumulative_units = prev_amt - quantity,
			transacted_value = dollar_value,
			previous_cost = previous_cost,
			cost_of_transaction = quantity / previous_units * previous_cost,
			cost_per_unit = previous_cost / previous_units,
			cumulative_cost = previous_cost - dollar_value,
			gain_loss = dollar_value - cost_of_transaction,
			realised_pct = gain_loss / cost_of_transaction
		)

	db_session.add(myTransaction)
	db_session.commit()
