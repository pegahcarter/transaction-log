import models
import exchange
import transactions

def rebalance(myPortfolio, df):

	# avgWeight = 1.0/len(myPortfolio.keys())
	avgWeight = 1.0/len(myPortfolio.coins)

	thresh = 0.01

	# dollar_values = map(lambda x: x['dollar_value'], myPortfolio)
	dollar_values = myPortfolio.dollar_values
	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_diffs = [
		avgWeight - min(dollar_values)/sum(dollar_values),
		max(dollar_values)/sum(dollar_values) - avgWeight
	]

	if min(weight_diffs) < 2 * avgWeight * thresh:
		df.to_csv('../data/transactions/transactions.csv', index=False)
		return myPortfolio, df

	d_amt = min(weight_diffs) * sum(dollar_values)

	df = exchange.trade(d_amt, myPortfolio, df)

	return rebalance(myPortfolio, df)


if __name__ == '__main__':

	# myPortfolio = models.Portfolio()
	# df = transactions.initialize(myPortfolio)
	# transactions.refresh(myPortfolio, df)
	# rebalance(myPortfolio, df)


	myPortfolio = models.Portfolio()
	df = transactions.initialize(myPortfolio)

	rebalance(myPortfolio, df)
