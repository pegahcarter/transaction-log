from constants import *
from models import Portfolio
import transactions
import exchange

TRADE_THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.15 # ensure that our trade is less than 10% of our total value
					   # because if it is, we need to fix the algo


def run(coins=None):

	portfolio = Portfolio(coins)
	avg_weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	trade_weight = min([avg_weight - min(portfolio.d_vals)/sum(portfolio.d_vals),
						max(portfolio.d_vals)/sum(portfolio.d_vals) - avg_weight])

	if trade_weight > MAX_TRADE_VALUE:
		print('Attempted to trade {} percent of total portfolio value.  Ending rebalance.'.format(MAX_TRADE_VALUE))
		return # TODO: how to end all rebalancing?
	elif trade_weight < avg_weight * TRADE_THRESHOLD:
		return portfolio

	d_amt = trade_weight * sum(portfolio.d_vals)
	exchange.trade(d_amt, portfolio, simulated) # TODO: add @param to recognize simulation for trade

	return run(coins, simulated)


if __name__ == '__main__':

	transactions.initialize()
	run()
	print('Coin values are within the acceptable threshold.  Rebalance complete!')
