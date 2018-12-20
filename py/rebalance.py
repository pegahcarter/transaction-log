from helper_functions import *

def rebalance():

	myPortfolio = Portfolio()
	n = 1/len(myPortfolio.coins)
	thresh = 0.02

	d_vals = myPortfolio.dollar_values
	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_diffs = [n - min(d_vals)/sum(d_vals), max(d_vals)/sum(d_vals) - n]

	if min(weight_diffs) < 2 * n * thresh:
		return

	d_amt = min(weight_diffs) * sum(d_vals)

	execute_trade(d_amt, myPortfolio)

	return rebalance()


if __name__ == '__main__':

	init_transactions()
	# rebalance()
