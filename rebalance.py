import os
import sys
import time
import pandas as pd
import numpy as np
import ccxt
from database import engine
from functions import coin_price

with open('api.txt', 'r') as f:
	api = f.readlines()
	apiKey = api[0][:len(api[0])-1]
	secret = api[1][:len(api[1])]

thresh = 0.01

try:
	while True:
		exchange = ccxt.binance({
			'options': {'adjustForTimeDifference': True},
			'apiKey': apiKey,
			'secret': secret
		})

		balance = exchange.fetchBalance()

		# update coin information
		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]
			# NOTE: are the parenthesis necessary?

		n = 1/len(coins)

		# Quantity of each coin in our portfolio
		coin_amts = np.array([balance[coin]['total'] for coin in coins])

		# Total dollar value of each coin in our portfolio
		d_vals = np.array([coin_amts[i] * coin_price(coins[i]) for i in range(len(coins))])

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

except:
	sys.exit('Error connecting to API socket.  Please ensure you are opening the \
		      correct api text file and are not using a network proxy, and try again')
