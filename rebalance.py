import os
import sys
import time
import pandas as pd
import numpy as np
from database import init_db, db_session, engine
from models import Transaction
from functions import exchange, coin_price

thresh = 0.01

try:

	while True:
		balance = exchange.fetchBalance()

		# update coin information
		coins = [asset['asset']
				 for asset in balance['info']['balances']
				 if float(asset['free']) > 0.01 and asset['asset'] != 'GAS']

		n = 1/len(coins)

		quantities, dollar_values = [], []

		quantities = np.array([balance[coin]['total'] for coin in coins])
		d_vals = np.array([quantities[i] * coin_price(coins[i]) for i in range(len(coins))])

		if (d_vals.max() - d_vals.min()) / d_vals.sum() < 2 * n * thresh:
			break

		# Determine if there's a trade ratio between the coins, or if we need to convert to BTC first
		ticker, side = determine_ticker(coins[dollar_values.argmin()], coins[dollar_values.argmax()])

		# Reference so that BTC won't be documented in the dual trade.
		dual_trade = None
		if len(ticker) > 1:
			dual_trade = True






except:
	sys.exit('Error connecting to API socket.  Please ensure you are opening the \
		   correct api text file and are not using a network proxy, and try again')





	weight_to_move = min([dollar_values.max()/dollar_values.sum() - n, n - dollar_values.min()/dollar_values.sum()])
	trade_dollars = weight_to_move * dollar_values.sum()

	for x in range(0,len(tickers),2):
		ratio = tickers[x]
		trade_coins = ratio.split('/')

		# Easier way to reference both coins in our dollar_values list at the same time
		indices = [coins.index(trade_coins[0]), coins.index(trade_coins[1])]
		trade_quantities = trade_dollars / (dollar_values[indices] / quantities[indices])

		# Make trade with quantity of numerator
		exchange.create_order(ratio, 'market', side, trade_quantities[0])

		# Update SQL database
		transactions = Update(dual_trade, trade_coins, trade_sides, trade_quantities, transactions, session)
