import models
import transactions
import exchange

i = 0

def rebalance(portfolio, df):

	avgWeight = 1.0/len(portfolio.coins)
	thresh = 0.01
    i += 1
	dollar_values = portfolio.dollar_values

	# We'll take the coins with the highest and lowest dollar value to
	# test our threshold
	weight_to_move = min([
		avgWeight - min(dollar_values)/sum(dollar_values),
		max(dollar_values)/sum(dollar_values) - avgWeight
	])

    if weight_to_move < thresh or i > 5:
        if transactions.new_transaction(df):
		    df.to_csv('../data/transactions/transactions.csv', index=False)
        if i > 5:
            print('Trade limit reached')

        return portfolio, df

	d_amt = min(weight_diffs) * sum(dollar_values)
    exchange.trade(d_amt, portfolio, df)

	return rebalance(portfolio, df)


if __name__ == '__main__':

	myPortfolio = models.Portfolio()
	df = transactions.initialize(myPortfolio)
	rebalance(myPortfolio, df)
