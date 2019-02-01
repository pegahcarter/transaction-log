import pandas as pd
import numpy as np
import transactions
import models

i = 24
INTERVAL = 'daily'


def simulate():   # TODO: add coins, interval, and interval string parameter
                  # NOTE: currently using 'i' for interval, and 'interval' for interval string

    # BTC, ETH, XRP, LTC, XLM coins to start
    coins = ['BTC','ETH','XRP','LTC','XLM']


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

    simulations[INTERVAL] = hr_totals

    simulations.to_csv('../data/simulations/simulations.csv', index=False)
    df.to_csv('../data/simulations/transactions.csv', index=False)


# NOTE: do I need this function here when I have a rebalance function in rebalance.py?
def rebalance(date, myPortfolio, currentPrices, df):

    d_vals = currentPrices * myPortfolio.units
    avg_weight = 1/len(currentPrices)
    # See how far the lightest and heaviest coin weight deviates from average weight
    weight = min([avg_weight - min(d_vals)/sum(d_vals),
                        max(d_vals)/sum(d_vals) - avg_weight])

    if 0.01 > weight: # note: 0.01 is the same as 0.05 threshold w/ 0.20 weights
        return myPortfolio, df

    tradeInDollars = weight * sum(d_vals)
    coinIndices = d_vals.argmin(), d_vals.argmax()
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
