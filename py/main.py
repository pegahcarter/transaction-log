import rebalance
import models
import transactions


if __name__ == '__main__':



	portfolio = models.Portfolio()
	weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	trade_weight = min([weight - min(portfolio.d_vals)/sum(portfolio.d_vals), max(portfolio.d_vals)/sum(portfolio.d_vals) - weight])

	if 20 > trade_weight * sum(portfolio.d_vals):
		print('No rebalance necessary')
	else:
		rebalance.run()
