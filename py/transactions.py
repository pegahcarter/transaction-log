import datetime
import pandas as pd
import numpy as np
import models
import exchange

'''
What do I want to do with transactions.csv?
    - First, there's the index issue
        > I want to use date as index
        > But I can't do that for simulations if there's more than one trade in
            an hour interval
        > I want rebalanced transactions and simulated transactions to have the
            same exact structure

transactions
    - CSV
        > column 0 = trade_num
        > column 1 = date of trade

    - DataFrame
        > index = trade_num
        > DF initialization issue
            - setting an index at first makes an N/A row
        > Easy way to append?

'''

transactions_file = '../data/transactions/transactions.csv'
sim_transactions_file = '../data/'
prices_file = '../data/historical/prices.csv'


def create():
    ''' Create our transactions CSV file if it doesn't yet exist '''

    myPortfolio = models.Portfolio()
    try:
        df = pd.read_csv(transactions_file)
    except:
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


    for coin in myPortfolio.coins:
        if coin not in df['coin']:
            df = add_coin(coin, exchange.price(coin), myPortfolio, df)

    if new_transaction(df):
        df.to_csv(transactions_file, index=False)

    return df


def new_transaction(df):
    try:
        if len(df) > len(pd.read_csv(transactions_file)):
            return True
    # Make an exception in case the transactions file has not been created before.
    # If it has not been created, the if statement above would create an error.
    except:
        return True
    else:
        return


def add_coin(coin, current_price, myPortfolio, df, date=None):
    ''' Add initial purchase of coin to transactions table '''

    units = myPortfolio.units[myPortfolio.coins.index(coin)]

    if date is None:
        date = datetime.datetime.now()
        current_price = exchange.price(coin)

    df = df.append({
        'date': date,
        'coin': coin,
        'side': 'buy',
        'units': units,
        'fees': current_price * units * 0.00075,
        'previous_units': 0,
        'cumulative_units': units,
        'transacted_value': current_price * units,
        'previous_cost': 0,
        'cumulative_cost': current_price * units
    }, ignore_index=True)

    return df


def update(coin, side, units, dollar_value, df, date=None):
    '''
    Document transaction data to SQL table

    coin            - coin we're documenting for the trade
    side            - side we're executing the trade on (buy or sell)
    units             - units of coin to be traded
    dollar_value    - value of our trade in dollars
    df              - transactions dataframe
    '''

    previous_units = df[df['coin'] == coin]['cumulative_units'].iloc[-1]
    previous_cost = df[df['coin'] == coin]['cumulative_cost'].iloc[-1]

    if date is None:
        date = datetime.datetime.now()
        current_price = exchange.price(coin)

    if side == 'buy':
        fees = dollar_value * 0.00075
        cumulative_units = previous_units + units
        cost_of_transaction = None
        cost_per_unit = None
        cumulative_cost = previous_cost + dollar_value
        gain_loss = None
        realised_pct = None
    else:
        fees = None
        cumulative_units = previous_units - units
        cost_of_transaction = units / previous_units * previous_cost
        cost_per_unit = previous_cost / previous_units
        cumulative_cost = previous_cost - dollar_value
        gain_loss = dollar_value - cost_of_transaction
        realised_pct = gain_loss / cost_of_transaction

    df = df.append({
        'date': date,
        'coin': coin,
        'side': side,
        'units': units,
        'fees': fees,
        'previous_units': previous_units,
        'cumulative_units': cumulative_units,
        'transacted_value': current_price * units,
        'previous_cost': previous_cost,
        'cost_of_transaction':  cost_of_transaction,
        'cost_per_unit': cost_per_unit,
        'cumulative_cost': cumulative_cost,
        'gain_loss': gain_loss,
        'realised_pct': gain_loss
    }, ignore_index=True)

    return df
