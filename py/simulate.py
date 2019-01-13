import datetime
import pandas as pd
import numpy as np
import transactions
import models

def simulate():   # TODO: add coins, interval, and interval string parameter
                  # NOTE: currently using 'i' for interval, and 'interval' for interval string


    # BTC, ETH, XRP, LTC, XLM coins to start
    coins = ['BTC','ETH','XRP','LTC','XLM']
    i = 24
    interval = 'daily'

    myPortfolio = models.SimPortfolio(coins)

    hist_prices = pd.read_csv('../data/historical/prices.csv')
    simulations = pd.DataFrame(index=hist_prices['timestamp'])

    hist_prices_array = np.array(hist_prices[coins])
    simulations['hodl'] = list(np.dot(hist_prices_array, myPortfolio.units))

    df = pd.DataFrame(columns=['date',
                               'coin',
                               'side',
                               'units',
                               'fees',
                               'previousUnits',
                               'cumulativeUnits',
                               'transactedValue',
                               'previousCost',
                               'costOfTransaction',
                               'costPerUnit',
                               'CumulativeCost',
                               'gainLost',
                               'realisedPct'])

    purchasePrices = hist_prices_array[0]
    for x, coin in enumerate(myPortfolio.coins):
        transactions.addCoin(coin,
                             purchasePrices[x],
                             myPortfolio,
                             df,
                             hist_prices['timestamp'][0])

    hr_totals = [5000]

    for hr in range(1, len(hist_prices)):
        if hr % i == 0:
            date = hist_prices['timestamp'][hr]
            myPortfolio, df = rebalance(date, myPortfolio, hist_prices_array[hr], df)

        hr_totals.append(np.dot(hist_prices_array[hr], myPortfolio.units))

    simulations[interval] = hr_totals

    simulations.to_csv('../data/simulations/simulations.csv')
    df.to_csv('../data/simulations/transactions.csv')


# NOTE: do I need this function here when I have a rebalance function in rebalance.py?
def rebalance(date, myPortfolio, currentPrices, df):

    dollarValues = currentPrices * myPortfolio.units
    avg_weight = 1/len(currentPrices)
    # See how far the lightest and heaviest coin weight deviates from average weight
    weightToMove = min([avg_weight - min(dollarValues)/sum(dollarValues),
                        max(dollarValues)/sum(dollarValues) - avg_weight])

    if 0.01 > weightToMove: # note: 0.01 is the same as 0.05 threshold w/ 0.20 weights
        return myPortfolio, df

    tradeInDollars = weightToMove * sum(dollarValues)
    coinIndices = dollarValues.argmin(), dollarValues.argmax()
    df = trade(date, tradeInDollars, coinIndices, currentPrices, myPortfolio, df)

    return rebalance(date, myPortfolio, currentPrices, df)


def trade(date, d_amt, coinIndices, currentPrices, myPortfolio, df):

    sides = 'buy', 'sell'
    # add to transactions
    for x, side in enumerate(sides):
        pos = coinIndices[x]
        coin = myPortfolio.coins[pos]
        units = (d_amt / currentPrices[pos])
        # Include a 1% slippage rate and 0.1% trading fee
        if side == 'buy':
            myPortfolio.units[pos] += (units * 0.989)
        else:
            myPortfolio.units[pos] -= units

        df = transactions.update(coin, side, units, d_amt, df, date, currentPrices[pos])

    return df

simulate()
