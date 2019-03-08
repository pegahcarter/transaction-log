import models
import transactions
import exchange
from crontab import CronTab

MAX_TRADE_VALUE = 200 # ensure that our trade is worth less than our upper limit

def run(coins=None):

	portfolio = models.Portfolio(coins)
	avg_weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	trade_weight = min([avg_weight - min(portfolio.d_vals)/sum(portfolio.d_vals),
						max(portfolio.d_vals)/sum(portfolio.d_vals) - avg_weight])

	d_amt = trade_weight * sum(portfolio.d_vals)
	
	if d_amt < 20:
		print('Trade value is less than $20.  Rebalance complete.')
		return

	exchange.trade(d_amt, portfolio) # TODO: add @param to recognize simulation for trade

	return run(coins)


if __name__ == '__main__':

	transactions.initialize()
	run()
