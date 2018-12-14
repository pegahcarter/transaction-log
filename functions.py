from database import db_session, engine, hist_prices
from models import Transaction
from exchange import exchange
import datetime

def coin_price(coin):
	'''Returns the current dollar price of the coin in question'''
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


def find_sides(numerator, l_coin):
	'''Returns a tuple where the tuple[0] is the side of our trade and tuple[1]
	is for when we document the other side of the trade

	numerator 	- coin before the '/' in the ticker
	l_coin		- coin with the lowest total $ value in our portfolio
	'''
	if numerator == l_coin:
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def find_quantities(ratio, d_amt):
	return d_amt/coin_price(ratio[0]), d_amt/coin_price(ratio[1])


def find_tickers(coins):
	'''Determines if there is an existing coin ratio to execute trade.
	If there isn't a ratio, convert	to BTC first (like XRP/OMG)
	'''
	try:
		exchange.fetch_ticker(coins[0] + '/' + coins[1])
		return [[coins[0], coins[1]]]
	except:
		try:
			exchange.fetch_ticker(coins[1] + '/' + coins[0])
			return [[coins[1], coins[0]]]
		except:
			return [[coins[0], 'BTC'], [coins[1], 'BTC']]


def update_transactions(coin, prev_amt, prev_cost, side, quantity, dollar_value):
	'''Documents transaction data to SQL table

	coin 			- coin we're documenting for the trade
	prev_amt 		- current quantity of the coin in our portfolio
	prev_cost 		- current total cost of the coin in our portfolio
	side 			- side we're executing the trade on (buy or sell)
	quantity 		- quantity of coin to be traded
	dollar_value 	- value of our trade in dollars
	'''

	if side == 'buy':
		cost_of_transaction = None
		cost_per_unit = None

		cumulative_cost = prev_cost + dollar_value
		cumulative_units = prev_amt + quantity
		gain_loss = None
		realised_pct = None

		fees = dollar_value * .001
	else:
		cost_of_transaction = quantity / prev_amt * prev_cost
		cost_per_unit = prev_cost / prev_amt

		cumulative_cost = prev_cost - dollar_value
		cumulative_units = prev_amt - quantity
		gain_loss = dollar_value - cost_of_transaction
		realised_pct = gain_loss / cost_of_transaction

		fees = None

	purchase_data = Transaction(
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

	# Push to SQL
	db_session.add(sim_purchase)
	db_session.commit()
