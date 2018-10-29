from templates.setup import Base, Transactions
from static.functions import coin_price
from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from datetime import datetime
import ccxt
import numpy as np
import pandas as pd
# import plotly
import os

exchange = ccxt.binance()


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

engine = create_engine('sqlite:///data/transactions.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

DBSession = sessionmaker(bind=engine)
session = DBSession()

# ------------------------------------------------------------------------------
@app.route('/')
def showTransactions():

	df = pd.read_sql(sql=''' SELECT * FROM transactions''', con=engine)
	coins = list(set(df['coin'].tolist()))
	portfolio = {}

	for coin in coins:
		temp = df.loc[df['coin'] == coin].reset_index(drop=True)
		units = temp['cumulative_units'][len(temp) - 1]
		cost = temp['cumulative_cost'][len(temp) - 1]
		cost_per_unit = units/cost

		last_price = coin_price(exchange, coin)
		unrealised_amt = (last_price - cost_per_unit) * units
		unrealised_pct = unrealised_amt / cost

		realised_amt = sum(temp.loc[temp['side'] == 'buy']['gain_loss'])
		gain_loss = unrealised_amt + realised_amt
		market_val = cost + unrealised_amt

		coin_data = {
			'last_price': last_price,
			'units': units,
			'cost': cost,
			'cost_per_unit': cost_per_unit,
			'unrealised_amt': unrealised_amt,
			'unrealised_pct': unrealised_pct,
			'realised_amt': realised_amt,
			'gain_loss': gain_loss,
			'market_val': market_val
		}

		portfolio[coin] = coin_data

	transactions = Transactions.query.all()
	return render_template('index.html', portfolio=portfolio, coins=coins, transactions=transactions)


if __name__ == "__main__":
	app.run(debug=True)
