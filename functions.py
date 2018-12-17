from database import refresh_df
from models import Transaction
import pandas as pd
import datetime
import ccxt

def coin_price(coin):
	'''Returns the current dollar price of the coin in question'''
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


def add_coin_to_transactions(coin, quantity, current_price):
	db_session.add(
		Transaction(
					date = datetime.datetime.now(),
					coin = coin,
					side = 'buy',
					units = quantity,
					price_per_unit = current_price,
					fees = current_price * quantity * 0.00075,
					previous_units = 0,
					cumulative_units = quantity,
					transacted_value = current_price * quantity,
					previous_cost = 0,
					cost_of_transaction = None,
					cost_per_unit = None,
					cumulative_cost = current_price * quantity,
					gain_loss = 0,
					realised_pct = None
		)
	)
	db_session.commit()


def execute_trade(d_amt, myPortfolio):

	tickers = find_tickers(myPortfolio)

	for ticker in tickers:
		df = refresh_df()

		sides = find_sides(ticker, myPortfolio)
		quantities = find_quantities(ticker, d_amt)

		exchange.create_order(symbol=ticker, type='market', side=sides[0], amount=quantities[0])

		for coin, side, quantity in zip(tickers.split('/'), sides, quantities):
			update_transactions(coin, side, quantity, d_amt)



def update_transactions(coin, side, quantity, dollar_value):
	'''Documents transaction data to SQL table

	coin 			- coin we're documenting for the trade
	side 			- side we're executing the trade on (buy or sell)
	quantity 		- quantity of coin to be traded
	dollar_value 	- value of our trade in dollars
	'''

	df = refresh_df()
	prev_amt, prev_cost = df[df['coin'] == coin][['cumulative_units', 'cumulative_cost']].iloc[-1, :]

	if side == 'buy':
		cost_of_transaction = None
		cost_per_unit = None

		cumulative_cost = prev_cost + dollar_value
		cumulative_units = prev_amt + quantity
		gain_loss = None
		realised_pct = None

		fees = dollar_value * .0075
	else:
		cost_of_transaction = quantity / prev_amt * prev_cost
		cost_per_unit = prev_cost / prev_amt

		cumulative_cost = prev_cost - dollar_value
		cumulative_units = prev_amt - quantity
		gain_loss = dollar_value - cost_of_transaction
		realised_pct = gain_loss / cost_of_transaction

		fees = None

	db_session.add(
		Transaction(
					date = datetime.datetime.now(),
					coin = coin,
					side = side,
					units = quantity,
					price_per_unit = coin_price(coin),
					fees = fees,
					previous_units = prev_amt,
					cumulative_units = cumulative_units,
					transacted_value = dollar_value,
					previous_cost = prev_cost,
					cost_of_transaction = cost_of_transaction,
					cost_per_unit = cost_per_unit,
					cumulative_cost = cumulative_cost,
					gain_loss = gain_loss,
					realised_pct = realised_pct
		)
	)
	db_session.commit()
