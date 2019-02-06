from pathlib import Path
from rebalance import rebalance
import models

TRANSACTIONS_FILE = '../data/transactions/transactions.csv'

if __name__ == '__main__':

	if Path(TRANSACTIONS_FILE).exists() is False:
		transactions.initialize()

	portfolio = models.Portfolio()
	weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	trade_weight = min([weight - min(portfolio.d_vals)/sum(portfolio.d_vals), max(portfolio.d_vals)/sum(portfolio.d_vals) - weight])

	if 20 > trade_weight * sum(portfolio.d_vals):
		print('No rebalance necessary')
	elif 100 < trade_weight * sum(portfolio.d_vals):
		print('Error: trade exceeding $100.')
	else:
		rebalance()
