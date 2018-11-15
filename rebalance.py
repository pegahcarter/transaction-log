# TODO: Find an easy way to initialize the transactions table and create the
#		initial transactions without having to check if the table exists every time
#		I'll worry about that later, first focus on update function

import os
import sys
import time
import ccxt
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import init_db, db_session, engine
from models import Transaction
from functions import exchange, coin_price



try:


	while True:
		balance = exchange.fetchBalance()

		# update coin information
		coins = [asset['asset']
				 for asset in balance['info']['balances']
				 if float(asset['free']) > 0.01 and asset['asset'] != 'GAS']

		quantities, dollar_values = [], []

		quantities = np.array([balance[coin]['total'] for coin in coins])
		d_vals = np.array([quantities[i] * coin_price(coins[i]) for i in range(len(coins))])



		for coin in coins:
			quantity = balance[coin]['total']
			quantities.append(quantity)
			dollar_values.append(quantity * coin_price(exchange, coin))





except:
	sys.exit('Error connecting to API socket.  Please ensure you are opening the \
		   correct api text file and are not using a network proxy, and try again')


n = 1/(len(coins))
thresh = .02
i = 0





	# Line comprehension of above loop - should I use this instead and make another
	# line comprehension for quantities? Or is it better visually to keep the current method?
	# dollar_values = np.array([balance[coin]['total'] * coin_price(coin) for coin in coins])

	# Convert our lists to np arrays since our lists don't work well with mathematical operations
	quantities = np.array(quantities)
	dollar_values = np.array(dollar_values)

	if (dollar_values.max() - dollar_values.min()) / dollar_values.sum() < 2 * n * thresh:
		break




	# Determine if there's a trade ratio between the coins, or if we need to convert to BTC first
	tickers = determine_ticker(exchange, coins[dollar_values.argmin()], coins[dollar_values.argmax()])

	# Reference so that BTC won't be documented in the dual trade.
	if len(tickers) > 2:
		dual_trade = True
	else:
		dual_trade = False

	weight_to_move = min([dollar_values.max()/dollar_values.sum() - n, n - dollar_values.min()/dollar_values.sum()])
	trade_dollars = weight_to_move * dollar_values.sum()

	for x in range(0,len(tickers),2):
		ratio = tickers[x]
		trade_coins = ratio.split('/')

		side = tickers[x+1]
		if side == 'sell':
			trade_sides = ['sell', 'buy']
		else:
			trade_sides = ['buy', 'sell']

		# Easier way to reference both coins in our dollar_values list at the same time
		indices = [coins.index(trade_coins[0]), coins.index(trade_coins[1])]
		trade_quantities = trade_dollars / (dollar_values[indices] / quantities[indices])

		# Make trade with quantity of numerator
		exchange.create_order(ratio, 'market', side, trade_quantities[0])

		# Update SQL database
		transactions = Update(dual_trade, trade_coins, trade_sides, trade_quantities, transactions, session)

print('Rebalance complete.')
print('# of trades executed: ', i)
# Print trades that are executed
if i > 0:
	print(transactions.loc[transactions['trade_num'] > max(transactions['trade_num'] - 1)])
time.sleep(10)
