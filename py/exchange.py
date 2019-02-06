import ccxt
import transactions


def connect():
	''' Connect to our exchange API and fetch our account balance '''

	with open('../../../administrative/api.txt', 'r') as f:
		api = f.readlines()
		apiKey = api[0][:-1]
		secret = api[1]
	exchange = ccxt.binance({'options': {'adjustForTimeDifference': True},
							 'apiKey': apiKey,
							 'secret': secret})

	return exchange


binance = connect()


def fetch_price(coin):
	''' Return the current dollar price of the coin in question '''

	btc_price = float(binance.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		return btc_price
	else:
		btc_ratio = float(binance.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		return btc_ratio * btc_price


def trade(d_amt, portfolio):
	''' Execute trade on exchange to rebalance, and document said trade to transactions	'''

	tickers = findTickers(portfolio)
	print('Dollar value: ${}'.format(round(d_amt, 2)))
	if len(tickers) == 2:
		print("Conversion to BTC needed.")

	for ticker in tickers:
		print(ticker)
		coins = ticker.split('/')
		sides = findSides(ticker, portfolio)
		units = findUnits(ticker, d_amt)
		binance.create_order(symbol=ticker,
							 type='market',
							 side=sides[0],
							 amount=units[0])

		transactions.update(coins, sides, units, d_amt)

	return portfolio


def findTickers(portfolio):
	'''
	Determine the coin pair needed to execute the trade.
	If there isn't a pair, convert to BTC first
	(i.e. XRP/OMG becomes XRP/BTC and OMG/BTC)
	'''

	coin1 = portfolio.coins[portfolio.d_vals.argmin()]
	coin2 = portfolio.coins[portfolio.d_vals.argmax()]

	try:
		binance.fetch_ticker(coin1 + '/' + coin2)
		return [coin1 + '/' + coin2]
	except:
		try:
			binance.fetch_ticker(coin2 + '/' + coin1)
			return coin2 + '/' + coin1
		except:
			return [coin2 + '/BTC', coin1 + '/BTC']


def findSides(ticker, portfolio):
	'''
	Return a tuple where the tuple[0] is the side of our trade and tuple[1]
	is for documenting the other side of the trade

	ticker - the coin we are buying and the coin we are selling, combined by '/'
	'''

	numerator = ticker[:ticker.find('/')]
	if portfolio.coins.index(numerator) == portfolio.d_vals.argmin():
		return 'buy', 'sell'
	else:
		return 'sell', 'buy'


def findUnits(ticker, d_amt):

	numerator, denominator = ticker.split('/')

	return d_amt/fetch_price(numerator), d_amt/fetch_price(denominator)
