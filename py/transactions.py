import exchange
import time
import pandas as pd
from models import Portfolio

hist_prices = pd.read_csv('../data/historical/prices.csv')
START_DATE = int(hist_prices['timestamp'][0])


COLUMNS = ['date', 'coin', 'side', 'units', 'pricePerUnit', 'fees', 'previousUnits',
           'cumulativeUnits', 'transactedValue', 'previousCost', 'costOfTransaction',
           'costOfTransactionPerUnit', 'cumulativeCost', 'gainLoss', 'realisedPct']


def initialize(TRANSACTIONS_FILE, PORTFOLIO_START_VALUE=None, coins=None):
    ''' Create transactions.csv'''
    try:
        df = pd.read_csv(TRANSACTIONS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(TRANSACTIONS_FILE, index=False)

    portfolio = Portfolio(coins, PORTFOLIO_START_VALUE)
    for coin, coinUnits in zip(portfolio.coins, portfolio.units):
        if df.empty or coin not in set(df['coin']):
            addCoin(coin, coinUnits, TRANSACTIONS_FILE, PORTFOLIO_START_VALUE)

    return


def addCoin(coin, coinUnits, TRANSACTIONS_FILE, PORTFOLIO_START_VALUE=None):
    ''' Add initial purchase of coin to transactions table '''

    if PORTFOLIO_START_VALUE is None:
        date = time.time()
        price = exchange.fetch_price(coin)
    else:
        date = START_DATE
        price = hist_prices[coin][0]

    df = pd.read_csv(TRANSACTIONS_FILE)
    df = df.append({'date': date,
                    'coin': coin,
                    'side': 'buy',
                    'units': coinUnits,
                    'pricePerUnit': price,
                    'fees': price * coinUnits * 0.00075,
                    'previousUnits': 0,
                    'cumulativeUnits': coinUnits,
                    'transactedValue': price * coinUnits,
                    'previousCost': 0,
                    'cumulativeCost': price * coinUnits,
                    'gainLoss': 0}, ignore_index=True)

    df.to_csv(TRANSACTIONS_FILE, index=False)

    return


def update(coins, sides, coinUnits, d_amt, date=None, currentPrice=None):
    '''
    Document transaction data to CSV

    coin            - coin we're documenting for the trade
    side            - side we're executing the trade on (buy or sell)
    coinUnits       - units of coin to be traded
    d_amt           - value of our trade in dollars
    '''

    for coin, tradeSide, tradeUnits in zip(coins, sides, coinUnits):

        if date is None:
            date = time.time()
            currentPrice = exchange.fetch_price(coin)

        df = pd.read_csv(TRANSACTIONS_FILE)
        previousUnits = df[df['coin'] == coin]['cumulativeUnits'].iloc[-1]
        previousCost = df[df['coin'] == coin]['cumulativeCost'].iloc[-1]

        if tradeSide == 'buy':
            fees = d_amt * 0.00075
            cumulativeUnits = previousUnits + tradeUnits
            costOfTransactionPerUnit = None
            costOfTransaction = None
            cumulativeCost = previousCost + d_amt
            gainLoss = None
            realisedPct = None
        else:
            fees = None
            cumulativeUnits = previousUnits - tradeUnits
            costOfTransactionPerUnit = previousCost / previousUnits
            costOfTransaction = tradeUnits / previousUnits * previousCost
            cumulativeCost = previousCost - d_amt
            gainLoss = d_amt - costOfTransaction
            realisedPct = gainLoss / costOfTransaction

        df = df.append({'date': date,
                        'coin': coin,
                        'side': tradeSide,
                        'units': tradeUnits,
                        'pricePerUnit': currentPrice,
                        'fees': fees,
                        'previousUnits': previousUnits,
                        'cumulativeUnits': cumulativeUnits,
                        'transactedValue': currentPrice * tradeUnits,
                        'previousCost': previousCost,
                        'costOfTransaction':  costOfTransaction,
                        'costOfTransactionPerUnit': costOfTransactionPerUnit,
                        'cumulativeCost': cumulativeCost,
                        'gainLoss': gainLoss,
                        'realisedPct': realisedPct}, ignore_index=True)

    # Save updated dataframe to CSV
    df.to_csv(TRANSACTIONS_FILE, index=False)

    return
