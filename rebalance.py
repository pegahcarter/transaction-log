import os
import sys
import time
import pandas as pd
import numpy as np
from models import Portfolio, Transaction
import database
from functions import coin_price

def rebalance():

	myPortfolio = Portfolio()
	n = 1/len(myPortfolio.coins)
	thresh = 0.02

	d_vals = myPortfolio.dollar_values
	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_diffs = [n - min(d_vals)/sum(d_vals), max(d_vals)/sum(d_vals) - n]

	if min(weight_diffs) < 2 * n * thresh:
		return

	d_amt = min(weight_diffs) * sum(d_vals)

	tickers = find_tickers(myPortfolio.outlier_coins())

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


	return rebalance()

# except:
# 	sys.exit('Error connecting to API socket.  Please ensure you are opening the \
# 		      correct api text file and are not using a network proxy, and try again')
