import models
import transactions
import exchange
from pathlib import Path


THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.10 # ensure that our trade is less than 10% of our total value
					   # because if it is, there's probably something wrong.

def run():

	portfolio = models.Portfolio()
	avg_weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	trade_weight = min([avg_weight - min(portfolio.d_vals)/sum(portfolio.d_vals),
						max(portfolio.d_vals)/sum(portfolio.d_vals) - avg_weight])

	if trade_weight < avg_weight * THRESHOLD:
		print('Coin values are within the acceptable threshold.  Rebalance complete!')
		return

	d_amt = trade_weight * sum(portfolio.d_vals)
	exchange.trade(d_amt, portfolio)

	return run()


if __name__ == '__main__':

	transactions.initialize()
	run()
