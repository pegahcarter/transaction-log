import transactions
import exchange

THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.05 # ensure that our trade is less than 5% of our total value
					   # because if it is, there's probably something wrong.

def rebalance(portfolio):

	avgWeight = 1.0/len(portfolio.coins)
	dollarValues = portfolio.dollarValues

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	weightToMove = min([avgWeight - min(dollarValues)/sum(dollarValues),
						max(dollarValues)/sum(dollarValues) - avgWeight])

	if weightToMove > MAX_TRADE_VALUE:
		print('Trade exceeding 5 percent of total portfolio value.  Stopping early.')
		return

	if weightToMove > THRESHOLD * avgWeight:
		portfolio = exchange.trade(weightToMove, portfolio)
		return rebalance(portfolio)
	else:
		return

if __name__ == '__main__':

	myPortfolio = transactions.initialize()
	rebalance(myPortfolio)

'''
- Should the CSV creation exist separately?
- Do I need to set up the initialize() function into an intitialization script
	that's either insie `__init__.py` or inside requirements.txt?
- Should this only be set up to run through a web page?
- This would be a cool smart contract for a DAO...
'''
