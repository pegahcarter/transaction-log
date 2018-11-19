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


def determine_sides(ticker):
	if ticker.split('/')[0] == light_coin:
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def determine_quantities(ticker, d_amt):
	coin1, coin2 = ticker.split('/')
	return d_amt/coin_price(coin1), d_amt/coin_price(coin2)


def determine_ticker(coin1, coin2):
	'''Determine existing coin ratio to execute trade and convert
	to BTC first if there isn't a ratio (like XRP/OMG)
	'''
	try:
		exchange.fetch_ticker(coin1 + '/' + coin2)
		return [coin1 + '/' + coin2]
	except:
		try:
			exchange.fetch_ticker(coin2 + '/' + coin1)
			return [coin2 + '/' + coin1]
		except:
			return [coin1 + '/' + coin2, coin2 + '/' + coin1]



def update_transactions(tickers, dollar_amt):
	'''Documents transaction data to SQL table
	tickers - list of either one coin ratio or two
	dollar_amt - dollar value of trade
	'''

	sides = determine_sides(tickers[0])
	quantities = determine_quantities(tickers[0], dollar_amt)


	for coin, side, quantity in zip(tickers[0].split('/'), sides, quantities[0]):





	# Slowly fill in the ...'s once I have the values for the variables

		purchase_data = Transaction(
			date = datetime.datetime.now(),
			coin = coin,
			side = ...,
			units = ...,
			price_per_unit = coin_price(coin),
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



	if len(tickers) > 1:
		 return update_transactions(tickers[1], d_amt)



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


'''
