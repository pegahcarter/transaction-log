import constants
import models
import transactions
import exchange


def run(coins=None, simulated=None):

	if coins:
		portfolio = models.Portfolio(coins)
	else:
		portfolio = models.Portfolio()

	avg_weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	trade_weight = min([avg_weight - min(portfolio.d_vals)/sum(portfolio.d_vals),
						max(portfolio.d_vals)/sum(portfolio.d_vals) - avg_weight])

	if trade_weight < avg_weight * TRADE_THRESHOLD:
		return

	d_amt = trade_weight * sum(portfolio.d_vals)
	exchange.trade(d_amt, portfolio, simulated)

	return run(coins, simulated)


if __name__ == '__main__':

	transactions.initialize()
	run()
	print('Coin values are within the acceptable threshold.  Rebalance complete!')
