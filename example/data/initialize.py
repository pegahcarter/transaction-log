import datetime
import pandas as pd
import numpy as np
import os
import sys
import ccxt
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup import Transactions, Base

# BTC, ETH, XRP, LTC coins to start
coins = ['BTC','ETH','XRP','LTC']

# Date range - use median of starting mcap / ending mcap
hist_cap = pd.read_csv('historical_market_cap.csv')
hist_cap = np.array(hist_cap)

start_dates = hist_cap[:len(hist_cap) - 365]
end_dates = hist_cap[365:]

cap_diffs = list(end_dates[:, 3] - start_dates[:, 3])
if len(cap_diffs) % 2 == 0:
	cap_diffs.pop(len(cap_diffs) - 1)

# Start date for simulations
start_date = 0

hist_prices = pd.read_csv('../data/historical_prices.csv')
dates = hist_prices['date']
hist_prices = np.array(hist_prices[coins])

# Limit to current date range
hist_prices = hist_prices[start_date:start_date + 365]
dates = dates[start_date:start_date + 365]

start_amt = 5000
amt_each = start_amt / len(coins)

starting_prices = hist_prices[0]
purchase_date = datetime.datetime.fromtimestamp(dates[0])

db = 'transactions.db'
engine = create_engine('sqlite:///' + db)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

for i in range(len(coins)):
	price = starting_prices[i]
	quantity = amt_each / price

	coin = coins[i]

	session.add(Transactions(
		date = purchase_date,
		coin = coin,
		side = 'buy',
		units = quantity,
		price_per_unit = price,
		fees = amt_each * 0.0075,
		previous_units = 0,
		cumulative_units = quantity,
		transacted_value = amt_each,
		previous_cost = 0,
		cost_of_transaction = 0,
		cost_per_unit = 0,
		cumulative_cost = amt_each,
		gain_loss = 0,
		realised_pct = 0
	))
	session.commit()
