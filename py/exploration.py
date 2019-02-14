# File used to create simulate code
from models import Portfolio
import pandas as pd
import transactions
import rebalance

FREQUENCY = 'daily'
INTERVAL = 24
coins = ['BTC','ETH','XRP','LTC','XLM'] # TODO: dynamic coins
PORTFOLIO_START_VALUE = 5000
hr_totals = [PORTFOLIO_START_VALUE]
TRANSACTIONS_FILE = '../data/simulations/transactions.csv'
hist_prices = pd.read_csv('../data/historical/prices.csv')[['timestamp'] + coins]


transactions.initialize(TRANSACTIONS_FILE, PORTFOLIO_START_VALUE, coins)

simulations = pd.DataFrame(columns=['timestamp', 'hodl', 'rebalanced'])



for index, row in prices.iterrows():
    if index % INTERVAL == 0:
        portfolio = rebalance.run(coins)

    # Append hodl total value

    # Append rebalanced total value







# ---------------------------------------------------------------------------
# Code from the old simulation repository
coins = hist_prices.columns[1:].tolist()

# convert our dataframe to numpy so we can find the dot product of quantities and prices
df = np.array(hist_prices[coins])

# run 250 simulations
for sim_num in range(250):

	# randomly select 5 coins to simulate
	random_coins = random.sample(coins, 5)
	coin_indices = [coins.index(coin) for coin in random_coins]
	df_small = df[:, coin_indices]

	# create portfolio class object
	myPortfolio = Portfolio(random_coins)

	# Combine the coin list with '-' to use as the column name
	col = '-'.join(random_coins)

	# Multiply quantities we own by hourly prices to get price for each hour
	sims[col] = list(np.dot(df_small, myPortfolio.quantities))
