import models
import exchange
import transactions

def rebalance(df):

	myPortfolio = models.Portfolio()
	n = 1.0/len(myPortfolio.coins)
	thresh = 0.01

	d_vals = myPortfolio.dollar_values
	print(myPortfolio.coins)
	print(d_vals)
	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_diffs = [n - min(d_vals)/sum(d_vals), max(d_vals)/sum(d_vals) - n]

	if max(weight_diffs) < 2 * n * thresh or i == 5:
		print(i)
		df.to_csv('../data/transactions/transactions.csv')
		return

	d_amt = min(weight_diffs) * sum(d_vals)

	df = exchange.trade(d_amt, myPortfolio, df)

	return rebalance(df)


if __name__ == '__main__':

	df = transactions.create()
	rebalance(df)
