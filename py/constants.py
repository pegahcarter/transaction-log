from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import ccxt

INTERVAL = 'daily'
HRS_BETWEEN_REBALANCING = 24
PORTFOLIO_START_VALUE = 5000
hr_totals = [PORTFOLIO_START_VALUE]
TRADE_THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.10 # ensure that our trade is less than 10% of our total value
					   # because if it is, we need to fix the algo
TRANSACTIONS_FILE = '../data/transactions/transactions.csv'
COLUMNS = ['date', 'coin', 'side', 'units', 'pricePerUnit', 'fees', 'previousUnits',
           'cumulativeUnits', 'transactedValue', 'previousCost', 'costOfTransaction',
           'costOfTransactionPerUnit', 'cumulativeCost', 'gainLoss', 'realisedPct']

api = ccxt.binance()
login = pd.read_csv('../api.csv')
binance = ccxt.binance({'options': {'adjustForTimeDifference': True},
                        'apiKey': login['apiKey'],
                        'secret': login['secret']})

hist_prices = pd.read_csv('../data/historical/prices.csv')
START_DATE = hist_prices['timestamp'][0]
coins = ['BTC','ETH','XRP','LTC','XLM'] # TODO: dynamic coins
