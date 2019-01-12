import models
import transactions
import exchange

THRESHOLD = 0.02
MAX_TRADE_VALUE = 0.05 # ensure that our trade is less than 5% of our total value
					   # because if it is, there's probably something wrong.

def rebalance():

	portfolio = models.Portfolio()
	# df = transactions.initialize(portfolio)

	avgWeight = 1.0/len(portfolio.coins)
	dollar_values = portfolio.dollar_values

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	weightToMove = min([
		avgWeight - min(dollar_values)/sum(dollar_values),
		max(dollar_values)/sum(dollar_values) - avgWeight
	])

	d_amt = weightToMove * sum(dollar_values)

	if weightToMove > MAX_TRADE_VALUE:
		print('Trade exceeding 5 percent of total portfolio value.  Stopping early.')
		return

	if weightToMove > THRESHOLD * avgWeight:
		exchange.trade(d_amt, portfolio)



		'''
		if transactions.new_transaction(df):
			df.to_csv('../data/transactions/transactions.csv', index=False)
			print('Updated transactions.csv')
			return
		'''

	# df = exchange.trade(d_amt, portfolio, df)


	return rebalance()


if __name__ == '__main__':

	rebalance()




'''
NOTE:

I don't need to load `df` in rebalance.py.  None of the functions nreed it other than
	in the line

	`
	if transactions.new_transaction(df):
		df.to_csv('../data/transactions/transactions.csv', index=False)

	return
	`

I feel like there's an easy way to validate if there's a new transaction
	without having to load in `df`...


'''
