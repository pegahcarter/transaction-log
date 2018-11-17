#TODO: figure out if I need to update exchange every time, or just fetchBalance()
from database import db_session, engine
from models import Transaction
from exchange import exchange
import datetime

def coin_price(coin):
	'''Returns the current dollar price of the coin in question'''
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	elif coin == 'DOGE':
		price = float(exchange.fetch_ticker('DOGE/USDT')['info']['lastPrice'])
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


def determine_ticker(coin1, coin2):
	'''Determine existing coin ratio to execute trade and convert
	to BTC first if there isn't a ratio (like XRP/OMG)
	'''
	try:
		exchange.fetch_ticker(coin1 + '/' + coin2)
		return [coin1 + '/' + coin2], ['buy']
	except:
		try:
			exchange.fetch_ticker(coin2 + '/' + coin1)
			return [coin2 + '/' + coin1], ['sell']
		except:
			return [coin1 + '/' + coin2, coin2 + '/' + coin1], ['buy','sell']

# Function to document transaction to sql
def update_transactions(dual_trade, coins, sides, quantities):
	'''Documents transaction data to SQL table
	dual_trade - Boolean,
	coins - list of either one coin ratio or two
	sides - list of either one side or two
	quantities - tuple of the coin quantities we're buying/selling

	'''


	# Plan for below:  Slowly fill in the ...'s once I have the values for the variables

	purchase_data = Transaction(
		date = datetime.datetime.now(),
		coin = ...,
		side = ...,
		units = ...,
		price_per_unit = ...,
		fees = ...,
		previous_units = ...,
		cumulative_units = ...,
		transacted_value = ...,
		previous_cost = ...,
		cost_of_transaction = ...,
		cost_per_unit = ...,
		cumulative_cost = ...,
		gain_loss = ...,
		realised_pct = ...
	)







'''
The tough part is that one trade is documented in different ways.

For example, let's say that we want to execute a trade to sell OMG for XRP.
That's __1__ trade.  But your exchange doesn't have that ratio, so you have to
have one trade to convert to BTC, and one trade to buy with BTC.  Now we're at __2__
trades.  For each trade, we can't just document the transaction from one coin to
the other.  We have to know what each price is in USD, so that when we end up selling
our crypto, we pay a boat load of taxes.  So instead of documenting the first trade
of selling the OMG for BTC, we have to first document the USD we sold the OMG for,
and the USD of the BTC we bought, at the price of the coin in that day at that time.






purchase_data = Transaction(
-	date = datetime.now(),
-	coin = coin,
-	side = side,
	units = quantity,
-	price_per_unit = coin_price(coin),
	fees = fees,
	previous_units = previous_units,
	cumulative_units = cumulative_units,
	transacted_value = d_amt,
	previous_cost = previous_cost,
	cost_of_transaction = cost_of_transaction,
	cost_per_unit = cost_per_unit,
	cumulative_cost = cumulative_cost,
	gain_loss = gain_loss,
	realised_pct = realised_pct
)

	if not dual trade:
		 return

	update_transactions(False, ..., ..., ...)
'''
