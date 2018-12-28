from datetime import datetime
import pandas as pd
from flask import Flask, request, render_template, redirect
import transactions
import models


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def showTransactions():


	myPortfolio = models.Portfolio()
	df = transactions.initialize()

	'''
	To add:
	if button on page is clicked:
		rebalance(myPortfolio, df)


	'''

	# Add additional dict/key values for coinDict
	myPortfolio.add_summary()




	for coin, current_price, coin_units in zip(myPortfolio.coins, myPortfolio.current_prices, myPortfolio.units):

		temp = df.loc[df['coin'] == coin].reset_index(drop=True)
		cost = temp['cumulative_cost'].iloc[-1]
		cost_per_unit = cost/coin_units
		unrealised_amt = (current_price - cost_per_unit) * coin_units
		realised_amt = sum(temp['gain_loss'].dropna())
		gain_loss = unrealised_amt + realised_amt
		market_val = coin_units * current_price

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
	return render_template('index.html', portfolio=myPortfolio, transactions=transactions)

# Close database connection as soon as an operation is complete
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

if __name__ == "__main__":
	app.run(debug=True)
