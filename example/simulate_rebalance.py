import os
import sys
import time
import ccxt
import pandas as pd
import numpy as np
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from py.setup import Transactions, Base
from py.functions import coin_price, determine_ticker
from py.update import Update


exchange = ccxt.bittrex()
tickers = set()
[tickers.add(ticker) for ticker in exchange.fetch_tickers()]

# BTC, ETH, XRP, BCH, LTC coins to start
coins = ['BTC','ETH','XRP','LTC']

# Date range - use median of starting mcap / ending mcap
hist_cap = pd.read_csv('data/historical_market_cap.csv')
hist_cap = np.array(hist_cap)

start_dates = hist_cap[:len(hist_cap) - 365]
end_dates = hist_cap[365:]

cap_diffs = list(end_dates[:, 3] - start_dates[:, 3])
if len(cap_diffs) % 2 == 0:
	cap_diffs.pop(len(cap_diffs) - 1)

# Start date for simulations
start_date = 0

hist_prices = pd.read_csv('data/historical_prices.csv')
dates = hist_prices['date']
hist_prices = np.array(hist_prices[coins])

# Limit to current date range
hist_prices = hist_prices[start_date:start_date + 365]
dates = dates[start_date:start_date + 365]

start_amt = 5000
amt_each = start_amt / len(coins)
avg_weight = 1 / len(coins)

starting_prices = hist_prices[0]
purchase_date = datetime.datetime.fromtimestamp(dates[0])

coin_amts = amt_each / starting_prices


for day in range(1, len(hist_prices)):
	d_vals = hist_prices_small[num_day] * coin_amts
	d_vals_total = sum(d_vals)
	l_index, h_index = d_vals.argmin(), d_vals.argmax()
	weight_to_move = min([avg_weight - d_vals[l_index]/d_vals_total, d_vals[h_index]/d_vals_total - avg_weight])

	if weighted_thresh > weight_to_move:
		break

	# Does a ticker for the coins exist? - if it doesn't, it needs to convert to BTC first, which takes two trades
	ratios = {coins[l_index] + '/' + coins[h_index], coins[h_index] + '/' + coins[l_index]}
	ticker = ratios & tickers

	


# Connect to our SQL database
db = 'transactions.db'
engine = create_engine('sqlite:////Users/Carter/Documents/Administrative/' + db)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

query = ''' SELECT * FROM transactions'''
transactions = pd.read_sql(sql=query, con=engine)

rebalance_num = transactions['rebalance_num'].max() + 1


n = 1/(len(coins))
thresh = .02
i = 0

while True:
	exchange = ccxt.binance({
		'options': {'adjustForTimeDifference': True},
		'apiKey': apiKey,
		'secret': secret})

	quantities, dollar_values = [], []
	for coin in coins:
		quantity = balance[coin]['total']
		quantities.append(quantity)
		dollar_values.append(quantity * coin_price(exchange, coin))

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
