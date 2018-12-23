# import models
# import exchange
# import transactions

def rebalance(df):

	myPortfolio = models.Portfolio()
	avg_weight = 1.0/len(myPortfolio.coins)
	thresh = 0.01

	d_vals = myPortfolio.dollar_values
	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_diffs = [
		avg_weight - min(d_vals)/sum(d_vals), max(d_vals)/sum(d_vals) - avg_weight
	]

	if max(weight_diffs) < 2 * n * thresh:
		df.to_csv('../data/transactions/transactions.csv')
		return

	d_amt = min(weight_diffs) * sum(d_vals)

	df = exchange.trade(d_amt, myPortfolio, df)

	return rebalance(df)


if __name__ == '__main__':

	transactions_file = '../data/transactions/transactions.csv'
	sim_transactions_file = '../data/'
	prices_file = '../data/historical/prices.csv'

	import models
	import exchange
	import transactions
	df = transactions.create()
	rebalance(df)
