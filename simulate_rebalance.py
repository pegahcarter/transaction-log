from database import db_session, engine, init_db
from models import Transaction
from functions import coin_price
from flask import Flask, request, render_template, redirect
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import datetime
import ccxt

# BTC, ETH, XRP, LTC coins to start
coins = ['BTC','ETH','XRP','LTC','BCH']

hist_prices = pd.read_csv('data/historical/prices.csv')
dates = hist_prices['date']
hist_prices = np.array(hist_prices[coins])

# Limit to one year of data
hist_prices = hist_prices[:365]
dates = dates[:365]

fees = 0
rate = 0.005
start_amt = 5000
thresh = 0.01
avg_weight = 1 / len(coins)
weighted_thresh = (avg_weight * thresh)

amt_each = start_amt / len(coins)
starting_prices = hist_prices[0]
coin_amts = amt_each / starting_prices

# Create our db
init_db()

# Simulate initial purchase of coins on day 0
day = datetime.fromtimestamp(dates[0])
for i in range(len(coins)):
	price = starting_prices[i]
	quantity = coin_amts[i]
	purchase = Transaction(
		date = day,
		coin = coins[i],
		side = 'buy',
		units = quantity,
		price_per_unit = price,
		fees = price * quantity * 0.0075,
		previous_units = 0,
		cumulative_units = quantity,
		transacted_value = price * quantity,
		previous_cost = 0,
		cost_of_transaction = None,
		cost_per_unit = None,
		cumulative_cost = price * quantity,
		gain_loss = 0,
		realised_pct = None
	)
	db_session.add(purchase)
	db_session.commit()


# Simulate daily rebalance for one year
for day in range(1, len(hist_prices)):
	purchase_date = datetime.fromtimestamp(dates[day])
	while True:

		# connect to db first
		transactions = pd.read_sql_table('transactions', con=engine)

		coin_amts = []
		# Update coin amounts
		for coin in coins:
			temp = transactions.loc[transactions['coin'] == coin, 'cumulative_units'].tolist()
			coin_amts.append(temp[len(temp)-1])

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

		d_amt = weight_to_move * d_vals_total
		trade_sides = ['buy','sell']
		trade_coins = [coins[l_index], coins[h_index]]

		# Get coin quantities to buy/sell based on current market price
		l_quantity = d_amt / hist_prices[day, l_index] * (1 - rate)
		h_quantity = d_amt / hist_prices[day, h_index]
		trade_quantities = [l_quantity, h_quantity]

		# Document trade
		for coin, side, units in zip(trade_coins, trade_sides, trade_quantities):

			temp = transactions.loc[transactions['coin'] == coin]
			previous_units = temp['cumulative_units'].values[len(temp)-1]
			previous_cost = temp['cumulative_cost'].values[len(temp)-1]


			if side == 'buy':
				cost_of_transaction = None
				cost_per_unit = None

				cumulative_cost = previous_cost + d_amt
				cumulative_units = previous_units + units
				gain_loss = None
				realised_pct = None

				fees = d_amt * .005

			else:
				cost_of_transaction = units / previous_units * previous_cost
				cost_per_unit = previous_cost / previous_units

				cumulative_cost = previous_cost - d_amt
				cumulative_units = previous_units - units
				gain_loss = d_amt - cost_of_transaction
				realised_pct = gain_loss / cost_of_transaction

				fees = None

			# push to SQL
			sim_purchase = Transaction(
				date = purchase_date,
				coin = coin,
				side = side,
				units = units,
				price_per_unit = hist_prices[day, coins.index(coin)],
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

			db_session.add(sim_purchase)
			db_session.commit()
