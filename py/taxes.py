import os
import sys
from datetime import datetime
import numpy as np
import pandas as pd
import ccxt
import transactions
import models
import exchange

df = pd.read_excel('../data/transactions/2018-binance.xlsx')

df.rename(columns={'Date(UTC)':'date', 'Fee Coin':'fee_coin'}, inplace=True)
df.columns = [col.lower() for col in df.columns]

df['date'] = [int(datetime.timestamp(datetime.strptime(day, '%Y-%m-%d %H:%M:%S')) * 1000) for day in df['date']]
df['market'] = [day[:3] + '/' + day[3:] for day in df['market']]

df.head()

for numer, denom in map(lambda x: x.split('/'), df['market']):
    print(x)
    print(y)



binance = ccxt.binance()
prices = binance.fetch_ohlcv(limit=1, since=epoch*1000, symbol='XRP/USDT')
for date, market, type, price, amount, total, fee, fee_coin in df.values:
    print(date)
