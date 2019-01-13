from datetime import datetime
import pandas as pd
import exchange
import models


TRANSACTIONS_FILE = '../data/transactions/transactions.csv'


def initialize():
    ''' Create our transactions CSV file if it doesn't yet exist '''

    try:
        portfolio = models.Portfolio()
        df = pd.read_csv(TRANSACTIONS_FILE)
    except:
        df = pd.DataFrame(columns=['date',
                                   'coin',
                                   'side',
                                   'units',
                                   'pricePerUnit',
                                   'fees',
                                   'previousUnits',
                                   'cumulativeUnits',
                                   'transactedValue',
                                   'previousCost',
                                   'costOfTransaction',
                                   'costOfTransactionPerUnit',
                                   'cumulativeCost',
                                   'gainLoss',
                                   'realisedPct'])

   for coin, coinUnits in zip(portfolio.coins, portfolio.units):
       if len(df) == 0 or coin not in set(df['coin']):
           df = addCoin(coin, coinUnits, df)

    return portfolio


def addCoin(coin, coinUnits, df, date=None, currentPrice=None):
    ''' Add initial purchase of coin to transactions table '''

    if date is None:
        date = datetime.now()
        currentPrice = exchange.price(coin)

    df = df.append({'date': date,
                    'coin': coin,
                    'side': 'buy',
                    'units': coinUnits,
                    'pricePerUnit': currentPrice,
                    'fees': currentPrice * coinUnits * 0.00075,
                    'previousUnits': 0,
                    'cumulativeUnits': coinUnits,
                    'transactedValue': currentPrice * coinUnits,
                    'previousCost': 0,
                    'cumulativeCost': currentPrice * coinUnits,
                    'gainLoss': 0}, ignore_index=True)

    df.to_csv(TRANSACTIONS_FILE)

    return


def update(coins, sides, coinUnits, d_amt, date=None, currentPrice=None):
    '''
    Document transaction data to CSV

    coin            - coin we're documenting for the trade
    side            - side we're executing the trade on (buy or sell)
    coinUnits       - units of coin to be traded
    dollarValue     - value of our trade in dollars
    df              - transactions dataframe
    '''

    df = pd.read_csv(TRANSACTIONS_FILE)
    for coin, side, coinUnits in zip(coins, sides, units):

        previousUnits = df[df['coin'] == coin]['cumulativeUnits'].iloc[-1]
        previousCost = df[df['coin'] == coin]['cumulativeCost'].iloc[-1]

        if date is None:
            date = datetime.now()
            currentPrice = exchange.price(coin)

        if side == 'buy':
            fees = dollarValue * 0.00075
            cumulativeUnits = previousUnits + units
            costOfTransactionPerUnit = None
            costOfTransaction = None
            cumulativeCost = previousCost + dollarValue
            gainLoss = None
            realisedPct = None
        else:
            fees = None
            cumulativeUnits = previousUnits - units
            costOfTransactionPerUnit = previousCost / previousUnits
            costOfTransaction = units / previousUnits * previousCost
            cumulativeCost = previousCost - dollarValue
            gainLoss = dollarValue - costOfTransaction
            realisedPct = gainLoss / costOfTransaction

        df = df.append({
            'date': date,
            'coin': coin,
            'side': side,
            'units': coinUnits,
            'pricePerUnit': currentPrice,
            'fees': fees,
            'previousUnits': previousUnits,
            'cumulativeUnits': cumulativeUnits,
            'transactedValue': currentPrice * units,
            'previousCost': previousCost,
            'costOfTransaction':  costOfTransaction,
            'costOfTransactionPerUnit': costOfTransactionPerUnit,
            'cumulativeCost': cumulativeCost,
            'gainLoss': gainLoss,
            'realisedPct': realisedPct
        }, ignore_index=True)

    # Save updated dataframe to CSV
    df.to_csv(TRANSACTIONS_FILE)

    return
