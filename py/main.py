if __name__ == '__main__':

	if Path(TRANSACTIONS_FILE).exists() is False:
		transactions.initialize()

	rebalance()
