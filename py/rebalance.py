import transactions
import exchange
import models

rebalance_needed = False
TRANSACTIONS_FILE = '../data/transactions/transactions.csv'
THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.10 # ensure that our trade is less than 10% of our total value
					   # because if it is, there's probably something wrong.

def rebalance():

	portfolio = models.Portfolio()
	avg_weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	trade_weight = min([avg_weight - min(portfolio.d_vals)/sum(portfolio.d_vals),
						max(portfolio.d_vals)/sum(portfolio.d_vals) - avg_weight])

	if trade_weight > MAX_TRADE_VALUE:
		print('Trade exceeding 10 percent of the total portfolio.  Stopping early.')
		return

	if trade_weight < avg_weight * THRESHOLD:
		print('Coin values are within the acceptable threshold.  Rebalance complete!')
		return

	d_amt = trade_weight * sum(portfolio.d_vals)
	exchange.trade(d_amt, portfolio)

	return rebalance()
