import transactions
import exchange
import models


THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.10 # ensure that our trade is less than 10% of our total value
					   # because if it is, there's probably something wrong.

def rebalance():

	portfolio = models.Portfolio()
	avgWeight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	weightToMove = min([avgWeight - min(portfolio.dollarValues)/sum(portfolio.dollarValues),
						max(portfolio.dollarValues)/sum(portfolio.dollarValues) - avgWeight])

	if weightToMove > MAX_TRADE_VALUE:
		print('Trade exceeding 10 percent of the total portfolio.  Stopping early.')
		return

	if weightToMove < avgWeight * THRESHOLD:
		print('Coin values are within the acceptable threshold.  Rebalance complete!')
		return

	d_amt = weightToMove * sum(portfolio.dollarValues)
	exchange.trade(d_amt, portfolio)

	return rebalance()


if __name__ == '__main__':

	transactions.initialize()
	rebalance()
