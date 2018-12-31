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
	TODO: add
	if button on page is clicked:
		rebalance(myPortfolio, df)


	'''

	# Add additional dict/key values for coinDict
	myPortfolio.add_summary()

	for coin in myPortfolio:
		pass


	transactions = Transaction.query.all()
	return render_template('index.html', portfolio=myPortfolio, transactions=transactions)

# Close database connection as soon as an operation is complete
@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

if __name__ == "__main__":
	app.run(debug=True)
