import ccxt

with open('api.txt', 'r') as f:
	api = f.readlines()
	apiKey = api[0][:len(api[0])-1]
	secret = api[1][:len(api[1])]

# NOTE: If you are using a different exchange than binance, modify the line below
exchange = ccxt.binance({
	'options': {'adjustForTimeDifference': True},
	'apiKey': apiKey,
	'secret': secret})
