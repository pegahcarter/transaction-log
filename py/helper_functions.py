import pandas as pd
import numpy as np
import datetime
import ccxt


def connect_to_exchange():
	''' Connect to our exchange API and fetch our account balance '''

	with open('../../api.txt', 'r') as f:
		api = f.readlines()
		apiKey = api[0][:-1]
		secret = api[1][:-1]

	exchange = ccxt.binance({
		'options': {'adjustForTimeDifference': True},
		'apiKey': apiKey,
		'secret': secret
	})
	return exchange


def coin_price(coin):
	''' Return the current dollar price of the coin in question '''

	exchange = connect_to_exchange()
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


def find_tickers(myPortfolio):
	'''
	Determine the coin pair needed to execute the trade.
	If there isn't a pair, convert to BTC first
	(i.e. XRP/OMG becomes XRP/BTC and OMG/BTC)
	'''

	exchange = connect_to_exchange()
	coin1 = myPortfolio.coins[myPortfolio.dollar_values.argmin()]
	coin2 = myPortfolio.coins[myPortfolio.dollar_values.argmax()]
	try:
		exchange.fetch_ticker(coin1 + '/' + coin2)
		return [[coin1, coin2]]
	except:
		try:
			exchange.fetch_ticker(coin2 + '/' + coin1)
			return [[coin2, coin1]]
		except:
			return [[coin1, 'BTC'], [coin2, 'BTC']]


def init_transactions():
	''' Create our transactions CSV file if it doesn't yet exist '''

	myPortfolio = Portfolio()
	try:
		df = pd.read_csv('../data/portfolio/transactions.csv')
	except:
		df = pd.DataFrame(columns=[
			'coin',
			'side',
			'units',
			'fees',
			'previous_units',
			'cumulative_units',
			'transacted_value',
			'previous_cost',
			'cost_of_transaction',
			'cost_per_unit',
			'cumulative_cost',
			'gain_loss',
			'realised_pct'
		])
		for coin in myPortfolio.coins:
			df = add_coin_to_transactions(coin, myPortfolio, df)

        df.to_csv('../data/transactions/transactions.csv')

	return df


def add_coin_to_transactions(coin, myPortfolio, transactions_df):
	''' Add initial purchase of coin to transactions table '''

	quantity = myPortfolio.quantities[myPortfolio.coins.index(coin)]
	current_price = coin_price(coin)

	transactions_df = transactions_df.append({
        'date': datetime.datetime.now(),
		'coin': coin,
		'side': 'buy',
		'units': quantity,
		'fees': current_price * quantity * 0.00075,
		'previous_units': 0,
		'cumulative_units': quantity,
		'transacted_value': current_price * quantity,
		'previous_cost': 0,
		'cumulative_cost': current_price * quantity
	}, ignore_index=True)

	return transactions_df


def update_transactions(coin, side, quantity, dollar_value, df):
	'''
	Document transaction data to SQL table

	coin 			- coin we're documenting for the trade
	side 			- side we're executing the trade on (buy or sell)
	quantity 		- quantity of coin to be traded
	dollar_value 	- value of our trade in dollars
	df				- transactions dataframe
	'''

	previous_units, previous_cost = df[df['coin'] == coin][['cumulative_units', 'cumulative_cost']].iloc[-1, :]

	if side == 'buy':
		fees = dollar_value * 0.00075
		cumulative_units = previous_units + quantity
		cost_of_transaction=None
		cost_per_unit=None
		cumulative_cost = previous_cost + dollar_value
		gain_loss=None
		realised_pct=None
	else:
		fees = None
		cumulative_units = prev_amt - quantity
		cost_of_transaction = quantity / previous_units * previous_cost
		cost_per_unit = previous_cost / previous_units
		cumulative_cost = previous_cost - dollar_value
		gain_loss = dollar_value - cost_of_transaction
		realised_pct = gain_loss / cost_of_transaction

	df = df.append({
        'date': datetime.datetime.now(),
		'coin': coin,
		'side': side,
		'units': quantity,
		'fees': fees,
		'previous_units': previous_units,
		'cumulative_units': quantity,
		'transacted_value': current_price * quantity,
		'previous_cost': previous_cost,
		'cost_of_transaction':  cost_of_transaction,
		'cost_per_unit': cost_per_unit,
		'cumulative_cost': cumulative_cost,
		'gain_loss': gain_loss,
		'realised_pct': gain_loss
	}, ignore_index=True)

	return df


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
	''' Execute trade on exchange to rebalance, and document said trade to transactions	'''

	exchange = connect_to_exchange()
	tickers = find_tickers(myPortfolio)

	for ticker in tickers:
		df = refresh_df()

		sides = find_sides(ticker, myPortfolio)
		quantities = find_quantities(ticker, d_amt)

		exchange.create_order(symbol=ticker, type='market', side=sides[0], amount=quantities[0])

		for coin, side, quantity in zip(tickers.split('/'), sides, quantities):
			update_transactions(coin, side, quantity, d_amt)


class Portfolio(object):
	'''
	Represents our account balance on Binance

	coins           - list of coin names we are invested in
	quantities      - list of the quantities for each coin held
	current_prices  - list of the most recent dollar price for each coin held
	dollar_values   - list of the dollar values for each coin held (quantities * current_prices)

	'''
	def __init__(self):

		exchange = connect_to_exchange()
		balance = exchange.fetchBalance()

		coins = [
			asset['asset']
			for asset in balance['info']['balances']
			if (float(asset['free']) > 0.01) and (asset['asset'] != 'GAS')
		]

		quantities = np.array([balance[coin]['total'] for coin in coins])
		current_prices = [coin_price(coin) for coin in coins]

		self.coins = coins
		self.quantities = quantities
		self.current_prices = current_prices
		self.dollar_values = quantities * current_prices
		# self.cost = []
		# self.cost_per_unit = []
		# self.unrealised_amt = []
		# self.unrealised_pct = []
		# self.realised_amt = []
		# self.gain_loss = []


class SimPortfolio(object):

	def __init__(self, coins):
		self.coins = coins
		hist_prices = pd.read_csv('../data/historical/prices.csv')
		self.quantities = [1000 / self.hist_prices[coin][0] for coin in coins]

	def execute_trade(self, coin_indices, dollar_amt, current_prices):
		buy_index, sell_index = coin_indices
		# Include a 1% slippage rate and 0.1% trading fee
		self.quantities[buy_index] += (dollar_amt / current_prices[buy_index] * 0.989)
		self.quantities[sell_index] -= (dollar_amt / current_prices[sell_index])
