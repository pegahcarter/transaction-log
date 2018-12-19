

def find_sides(ticker, myPortfolio):
	'''
	Return a tuple where the tuple[0] is the side of our trade and tuple[1]
	is for documenting the other side of the trade

	ticker 		- the coin we are buying and the coin we are selling, combined by '/'
	'''

	numerator = ticker[:ticker.find('/')]
	if myPortfolio.coins.index(numerator) == myPortfolio.dollar_values.argmin():
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def find_quantities(ticker, d_amt):
	numerator, denominator = ticker.split('/')
	return d_amt/coin_price(numerator), d_amt/coin_price(denominator)


def execute_trade(d_amt, myPortfolio):
	''' Execute trade on exchange to rebalance, and document said trade to transactions

	d_amt 			- dollar value of trade
	'''

	exchange = connect_to_exchange()
	tickers = find_tickers(myPortfolio)

	for ticker in tickers:
		df = refresh_df()

		sides = find_sides(ticker, myPortfolio)
		quantities = find_quantities(ticker, d_amt)

		exchange.create_order(symbol=ticker, type='market', side=sides[0], amount=quantities[0])

		for coin, side, quantity in zip(tickers.split('/'), sides, quantities):
			update_transactions(coin, side, quantity, d_amt)
