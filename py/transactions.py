from datetime import datetime
import pandas as pd
import exchange
import models


TRANSACTIONS_FILE = '../data/transactions/transactions.csv'


def refresh(df):

    portfolio = models.portfolio()
    for coin, coin_units in zip(portfolio.coins, portfolio.units):
        if coin not in set(df['coin']):
            addCoin(coin, coin_units, df)

    return portfolio


def initialize():
    ''' Create our transactions CSV file if it doesn't yet exist '''

    try:
        df = pd.read_csv(TRANSACTIONS_FILE)
    except:
        df = pd.DataFrame(columns=[
            'date',
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
            'realisedPct'
        ])

    refresh(df)

    return


def addCoin(coin, portfolio, df, date=None, currentPrice=None):
    ''' Add initial purchase of coin to transactions table '''

    if date is None:
        date = datetime.now()
        currentPrice = exchange.price(coin)

    df.append({
        'date': date,
        'coin': coin,
        'side': 'buy',
        'units': units,
        'pricePerUnit': currentPrice,
        'fees': currentPrice * units * 0.00075,
        'previousUnits': 0,
        'cumulativeUnits': units,
        'transactedValue': currentPrice * units,
        'previousCost': 0,
        'cumulativeCost': currentPrice * units,
        'gainLoss': 0
    }, ignore_index=True, inplace=True)
    df.to_csv(TRANSACTIONS_FILE)

    return


def update(coins, sides, units, d_amt, date=None, currentPrice=None):
    '''
    Document transaction data to CSV

    coin            - coin we're documenting for the trade
    side            - side we're executing the trade on (buy or sell)
    units           - units of coin to be traded
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
