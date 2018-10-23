import ccxt
# All additional functions used in rebalancing

# Function to get current coin price in $
def coin_price(exchange, coin):
	btc_price = float(exchange.fetch_ticker('BTC/USDT')['info']['lastPrice'])
	if coin == 'BTC':
		price = btc_price
	else:
		btc_ratio = float(exchange.fetch_ticker(coin + '/BTC')['info']['lastPrice'])
		price = btc_ratio * btc_price

	return price


# Function to determine ticker for trade and side of trade
# We need this because sometimes there's a direct ratio between the two coins,
# and sometimes there isn't.
def determine_ticker(exchange, coin1, coin2):
	try:
		exchange.fetch_ticker(coin1 + '/' + coin2)['info']
		return coin1 + '/' + coin2, 'sell'
	except:
		try:
			exchange.fetch_ticker(coin2 + '/' + coin1)['info']
			return coin2 + '/' + coin1, 'buy'
		except:
			return coin1 + '/BTC', 'sell', coin2 + '/BTC', 'buy'
