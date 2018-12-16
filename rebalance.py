import os
import sys
import time
import pandas as pd
import numpy as np
import models
import database
from functions import coin_price

def rebalance():

	myPortfolio = Portfolio()

	n = 1/len(coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_diffs = [n - min(d_vals)/sum(d_vals), max(d_vals)/sum(d_vals) - n]
	weight = min(weight_diffs)

	if weight < 2 * n * thresh:
		break

	d_amt = weight * sum(d_vals)

	# Names of coins we're trading
	coins_to_trade = coins[dollar_values.argmin()], coins[dollar_values.argmax()]

	# Determine if there's a trade ratio between the coins, or if we need
	# to convert to BTC first
	tickers = find_tickers(coins_to_trade)

	for ticker in tickers:
		df = pd.read_sql_table('transactions', con=engine)
		# TODO: function to add a new coin to table

		sides = find_sides(ticker[0], l_coin)
		quantities = find_quantities(ticker, d_amt)

		exchange.create_order(symbol=ticker, type='market', side=sides[0], amount=quantities[0])

		# update SQL database
		for coin, side, quantity in zip(ticker, sides, quantities):
			prev_amt, prev_cost = df[df['coin'] == coin][['cumulative_units', 'cumulative_cost']].iloc[-1, :]

			update_transactions(coin, prev_amt, prev_cost, side, quantity, d_amt)

# except:
# 	sys.exit('Error connecting to API socket.  Please ensure you are opening the \
# 		      correct api text file and are not using a network proxy, and try again')
