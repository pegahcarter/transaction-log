from database import init_db, refresh_df
from models import Transaction, Portfolio
from functions import coin_price
from flask import Flask, request, render_template, redirect
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def showTransactions():

	myPortfolio = init_db()
	df = refresh_df()


	for coin, current_price, quantity in zip(myPortfolio.coins, myPortfolio.current_prices, myPortfolio.quantities):

		temp = df.loc[df['coin'] == coin].reset_index(drop=True)
		cost = temp['cumulative_cost'][len(temp) - 1]
		cost_per_unit = cost/quantity
		unrealised_amt = (current_price - cost_per_unit) * quantity
		realised_amt = sum(temp['gain_loss'].dropna())
		gain_loss = unrealised_amt + realised_amt
		market_val = quantity * current_price

		myPortfolio.cost.append(cost)
		myPortfolio.cost_per_unit.append(cost_per_unit)
		myPortfolio.unrealised_amt.append(unrealised_amt)
		myPortfolio.realised_amt.append(realised_amt)
		myPortfolio.gain_loss.append(gain_loss)
		myPortfolio.market_val.append(market_val)


	# portfolio = {}
	# for coin in coins:
	# 	temp = df.loc[df['coin'] == coin].reset_index(drop=True)
	# 	units = temp['cumulative_units'][len(temp) - 1]
	# 	cost = temp['cumulative_cost'][len(temp) - 1]
	# 	cost_per_unit = cost/units
	#
	# 	last_price = coin_price(coin)
	# 	unrealised_amt = (last_price - cost_per_unit) * units
	# 	realised_amt = sum(temp['gain_loss'].dropna())
	# 	gain_loss = unrealised_amt + realised_amt
	#
	# 	market_val = cost + unrealised_amt
	# 	unrealised_pct = unrealised_amt / market_val
	#
	# 	coin_data = {
	# 		'last_price': last_price,
	# 		'units': units,
	# 		'cost': cost,
	# 		'cost_per_unit': cost_per_unit,
	# 		'unrealised_amt': unrealised_amt,
	# 		'unrealised_pct': unrealised_pct,
	# 		'realised_amt': realised_amt,
	# 		'gain_loss': gain_loss,
	# 		'market_val': market_val
	# 	}
	#
	# 	portfolio[coin] = coin_data

	transactions = Transaction.query.all()
	return render_template('index.html', portfolio=portfolio, coins=coins, transactions=transactions)

# Close database connection as soon as an operation is complete
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

if __name__ == "__main__":
	app.run(debug=True)
