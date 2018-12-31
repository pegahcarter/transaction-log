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


    df = pd.DataFrame(columns=[
        'date',
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

    purchase_prices = hist_prices_array[0]
    for x, coin in enumerate(myPortfolio.coins):
        transactions.add_coin(
            coin,
            purchase_prices[x],
            myPortfolio,
            df,
            hist_prices['timestamp'][0]
        )

    hr_totals = [5000]

    for hr in range(1, len(hist_prices)):
        if hr % i == 0:
            date = hist_prices['timestamp'][hr]
            myPortfolio, df = rebalance(date, myPortfolio, hist_prices_array[hr], df)

        hr_totals.append(np.dot(hist_prices_array[hr], myPortfolio.units))

    simulations[interval] = hr_totals

    simulations.to_csv('../data/simulations/simulations.csv')
    df.to_csv('../data/simulations/transactions.csv')


def rebalance(date, myPortfolio, current_prices, df):

    dollar_values = current_prices * myPortfolio.units
    avg_weight = 1/len(current_prices)

    # See how far the lightest and heaviest coin weight deviates from average weight
    weight_to_move = min([
        avg_weight - min(dollar_values)/sum(dollar_values),
        max(dollar_values)/sum(dollar_values) - avg_weight
    ])

    if 0.01 > weight_to_move: # note: 0.01 is the same as 0.05 threshold w/ 0.20 weights
        return myPortfolio, df

    trade_in_dollars = weight_to_move * sum(dollar_values)
    coin_indices = dollar_values.argmin(), dollar_values.argmax()

    df = trade(date, trade_in_dollars, coin_indices, current_prices, myPortfolio, df)

    return rebalance(date, myPortfolio, current_prices, df)


def trade(date, dollar_amt, coin_indices, current_prices, myPortfolio, df):

    sides = 'buy', 'sell'

    # add to transactions
    for x, side in enumerate(sides):

        pos = coin_indices[x]
        coin = myPortfolio.coins[pos]
        units = (dollar_amt / current_prices[pos])

        # Include a 1% slippage rate and 0.1% trading fee
        if side == 'buy':
            myPortfolio.units[pos] += (units * 0.989)
        else:
            myPortfolio.units[pos] -= units

        df = transactions.update(coin, side, units, dollar_amt, df, date, current_prices[pos])

    return df

simulate()
