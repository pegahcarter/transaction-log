import models
import transactions
import exchange

def rebalance(portfolio, df):

	avgWeight = 1.0/len(portfolio.coins)
	thresh = 0.01
	dollar_values = portfolio.dollar_values

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	weightToMove = min([
		avgWeight - min(dollar_values)/sum(dollar_values),
		max(dollar_values)/sum(dollar_values) - avgWeight
	])

	d_amt = weightToMove * sum(dollar_values)

	if d_amt < 30 or weightToMove < thresh:
		if transactions.new_transaction(df):
			df.to_csv('../data/transactions/transactions.csv', index=False)
			print('New transaction added.')

		return portfolio, df

	df = exchange.trade(d_amt, portfolio, df)

	return rebalance(portfolio, df)


if __name__ == '__main__':

	myPortfolio = models.Portfolio()
	df = transactions.initialize(myPortfolio)

	rebalance(myPortfolio, df)
