from pathlib import Path
from rebalance import rebalance

if __name__ == '__main__':

	if Path(TRANSACTIONS_FILE).exists() is False:
		transactions.initialize()

    if rebalance_needed:
        rebalance()
    else:
        return 'No rebalance necessary'
