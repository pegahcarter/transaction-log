from database import db_session, engine
from models import Transaction
import ccxt

exchange = ccxt.binance()

# Function to get current coin price in $
def coin_price(coin):
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price

def init_first_purchase(coin, date, price, quantity):

		purchase = Transaction(
		date = date,
		coin = coin,
		units = q,
		price_per_unit = p,
		fees = amt_each * 0.0075,
		previous_units = 0,
		cumulative_units = q,
		transacted_value = p * q,
		previous_cost = 0,
		cost_of_transaction = 0,
		cost_per_unit = 0,
		cumulative_cost = p * q,
		gain_loss = 0,
		realised_pct = 0
	)
	db_session.add(purchase)
	db_session.commit()
