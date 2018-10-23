import datetime
from py.setup import Transactions, Base
from py.functions import coin_price

# Function to populate SQL with coins that have no prior documented transactions
def Initialize(session, exchange, balance, coin):

	price = coin_price(exchange, coin)
	quantity = balance[coin]['total']
	dollar_value = quantity * price

	session.add(Transactions(
		rebalance_num = 0,
		date = datetime.datetime.now(),
		coin = coin,
		side = 'buy',
		units = quantity,
		price_per_unit = price,
		fees = dollar_value * 0.0075,
		previous_units = 0,
		cumulative_units = quantity,
		transacted_value = dollar_value,
		previous_cost = 0,
		cumulative_cost = dollar_value,
	))
	session.commit()
