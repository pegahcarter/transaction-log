import models
import transactions
import exchange

def rebalance(df):

	portfolio = models.Portfolio()
	avgWeight = 1.0/len(portfolio.coins)
	thresh = 0.02
	dollar_values = portfolio.dollar_values

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	weightToMove = min([
		avgWeight - min(dollar_values)/sum(dollar_values),
		max(dollar_values)/sum(dollar_values) - avgWeight
	])

	d_amt = weightToMove * sum(dollar_values)

	if weightToMove > 0.05:
		print('Stopping early.')
		return

	if weightToMove < thresh * avgWeight:
		if transactions.new_transaction(df):
			df.to_csv('../data/transactions/transactions.csv', index=False)
			print('Updated transactions.csv')

		return

	df = exchange.trade(d_amt, portfolio, df)

	return rebalance(df)


if __name__ == '__main__':

	portfolio = models.Portfolio()
	df = transactions.initialize(portfolio)
	rebalance(df)
