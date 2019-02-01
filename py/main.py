from pathlib import Path
from rebalance import rebalance
import models

if __name__ == '__main__':

	if Path(TRANSACTIONS_FILE).exists() is False:
		transactions.initialize()

	portfolio = models.Portfolio()
	weight = 1.0/len(portfolio.coins)

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold adf
	trade_weight = min([weight - min(portfolio.d_vals)/sum(portfolio.d_vals),
						max(portfolio.d_vals)/sum(portfolio.d_vals) - weight])

	if we
    if rebalance_needed:
        rebalance()
    else:
        print('No rebalance necessary')
