import transactions
import exchange

THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.10 # ensure that our trade is less than 5% of our total value
					   # because if it is, there's probably something wrong.

def rebalance():

	portfolio = models.Portfolio()
	avgWeight = 1.0/len(portfolio.coins)
	dollarValues = portfolio.dollarValues

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	weightToMove = min([avgWeight - min(dollarValues)/sum(dollarValues),
						max(dollarValues)/sum(dollarValues) - avgWeight])

	if weightToMove > avg_weight * MAX_TRADE_VALUE:
		print('Trade exceeding 10 percent relative to the average weight.  Stopping early.')
		return

	if weightToMove < avgWeight * THRESHOLD:
		print('Coin dollar values are within the acceptable threshold.  Rebalance complete!')
		return

	exchange.trade(weightToMove * sum(dollarValues), portfolio)
	return rebalance()


if __name__ == '__main__':

	transactions.initialize()
	transactions.refresh()
	rebalance()

'''
- Should the CSV creation exist separately?
- Do I need to set up the initialize() function into an intitialization script
	that's either insie `__init__.py` or inside requirements.txt?
- Should this only be set up to run through a web page?
- This would be a cool smart contract for a DAO...
'''
