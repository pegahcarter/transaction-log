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


fees = 0
rate = 0.0075
start_amt = 5000
thresh = 0.01
avg_weight = 1 / len(coins)
weighted_thresh = (avg_weight * thresh)
amt_each = start_amt / len(coins)

starting_prices = hist_prices[0]
purchase_date = datetime.datetime.fromtimestamp(dates[0])

coin_amts = amt_each / starting_prices

db = 'transactions.db'


for day in range(1, len(hist_prices)):
	date = datetime.datetime.fromtimestamp(dates[day])
	while True:
		# connect to db first
		engine = create_engine('sqlite:////Users/Carter/Documents/Github/rebalance-my-portfolio/example/data/' + db)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		query = ''' SELECT * FROM transactions'''
		transactions = pd.read_sql(sql=query, con=engine)

		# Declaring variables
		d_vals = hist_prices[day] * coin_amts
		d_vals_total = sum(d_vals)
		l_index, h_index = d_vals.argmin(), d_vals.argmax()
		weight_diffs = [avg_weight - d_vals[l_index]/d_vals_total, d_vals[h_index]/d_vals_total - avg_weight]
		weight_to_move = min(weight_diffs)

		# If the weighted_thresh is greater than the minimum weight difference,
		# We're close enough to stop rebalancing
		if weighted_thresh > min(weight_diffs):
			break

		d_amt = weight_to_move + d_vals_total
		trade_sides = ['buy','sell']
		trade_coins = [coins[l_index], coins[h_index]]

		fees += d_amt * rate
		# pretend we perfectly swap the coins and don't need a BTC intermediary trade
		# which side is which for the ticker
		# ASSUMPTION: trade rate will always be .0025, which means there's a perfect ratio
		# If we have to convert to BTC first, two trades will be executed, a.k.a. 0.005

		# the ratio of buy/sell will never matter
		# BECAUSE WE WILL ALWAYS BE BUYING THE (NOT LOWER WEIGHT) BUT COIN WITH THE
		# LOWEST WEIGHT, AND SELLING THE COIN OF HEAVIEST WEIGHT
		# Sell h_index(or coin with most weight)/buy l_index(or coin with least weight)

		# Get coin quantities to buy/sell based on current market price
		l_quantity = d_amt / hist_prices[day, l_index]
		h_quantity = d_amt / hist_prices[day, h_index] * (1 + rate)
		trade_quantities = [l_quantity, h_quantity]

		# Adjust coin quantities
		coin_amts[l_index] += l_quantity
		coin_amts[h_index] -= h_quantity

		# Document trade
		for coin, side, quantity in zip(trade_coins, trade_sides, trade_quantities):

			temp = transactions.loc[transactions['coin'] == coin]
			previous_units = temp['cumulative_units'].values[len(temp)-1]
			previous_cost = temp['cumulative_cost'].values[len(temp)-1]
			if side == 'buy':
				transacted_value = d_amt * (1 + .0075)
				cumulative_cost = previous_cost + transacted_value
				cumulative_units = previous_units + quantity
				# cost_of_transaction, cost_per_unit, gain_loss, realised_pct are N/A
				cost_of_transaction, cost_per_unit, gain_loss, realised_pct = None, None, None, None
			else:
				transacted_value = d_amt * (1 - .0075)
				cumulative_cost = previous_cost - transacted_value
				cumulative_units = previous_units - quantity
				cost_of_transaction = previous_cost * quantity/previous_units
				cost_per_unit = previous_cost / previous_units
				gain_loss = transacted_value - cost_of_transaction
				realised_pct = gain_loss / cost_of_transaction

				# push to SQL
			session.add(Transactions(
				date = date,
				coin = coin,
				side = side,
				units = quantity,
				price_per_unit = d_amt / quantity,
				fees = d_amt * .0075,
				previous_units = previous_units,
				cumulative_units = cumulative_units,
				transacted_value = transacted_value,
				previous_cost = previous_cost,
				cost_of_transaction = cost_of_transaction,
				cost_per_unit = cost_per_unit,
				cumulative_cost = cumulative_cost,
				gain_loss = gain_loss,
				realised_pct = realised_pct
			))
			session.commit()





transactions[3000:3005]


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
		# transactions = Update(dual_trade, trade_coins, trade_sides, trade_quantities, transactions, session)

print('Rebalance complete.')
