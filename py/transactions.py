import datetime
import pandas as pd
import numpy as np
import models
import exchange

def create():
    ''' Create our transactions CSV file if it doesn't yet exist '''

    myPortfolio = models.Portfolio()
    try:
        df = pd.read_csv('../data/portfolio/transactions.csv')
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

    coinAdded = None
    for coin in myPortfolio.coins:
        if coin not in df['coin']:
            df = add_coin(coin, Portfolio, df)
            coinAdded = True

    if coinAdded:
        df.to_csv('../data/portfolio/transactions.csv')

    return df


def add_coin(coin, myPortfolio, df, date=None, current_price=None):
    ''' Add initial purchase of coin to transactions table '''

    quantity = myPortfolio.quantities[myPortfolio.coins.index(coin)]

    if date is None:
        current_price = exchange.price(coin)

    df = df.append({
        'date': datetime.datetime.now(),
        'coin': coin,
        'side': 'buy',
        'units': quantity,
        'fees': current_price * quantity * 0.00075,
        'previous_units': 0,
        'cumulative_units': quantity,
        'transacted_value': current_price * quantity,
        'previous_cost': 0,
        'cumulative_cost': current_price * quantity
    }, ignore_index=True)

    return df


def update(coin, side, quantity, dollar_value, df, date=None, current_price=None):
    '''
    Document transaction data to SQL table

    coin             - coin we're documenting for the trade
    side             - side we're executing the trade on (buy or sell)
    quantity         - quantity of coin to be traded
    dollar_value     - value of our trade in dollars
    df                - transactions dataframe
    '''

    previous_units, previous_cost = df[df['coin'] == coin][['cumulative_units', 'cumulative_cost']].iloc[-1, :]

    if date is None:
        date = datetime.datetime.now()

    if side == 'buy':
        fees = dollar_value * 0.00075
        cumulative_units = previous_units + quantity
        cost_of_transaction=None
        cost_per_unit=None
        cumulative_cost = previous_cost + dollar_value
        gain_loss=None
        realised_pct=None
    else:
        fees = None
        cumulative_units = previous_units - quantity
        cost_of_transaction = quantity / previous_units * previous_cost
        cost_per_unit = previous_cost / previous_units
        cumulative_cost = previous_cost - dollar_value
        gain_loss = dollar_value - cost_of_transaction
        realised_pct = gain_loss / cost_of_transaction

    df = df.append({
        'date': date,
        'coin': coin,
        'side': side,
        'units': quantity,
        'fees': fees,
        'previous_units': previous_units,
        'cumulative_units': quantity,
        'transacted_value': current_price * quantity,
        'previous_cost': previous_cost,
        'cost_of_transaction':  cost_of_transaction,
        'cost_per_unit': cost_per_unit,
        'cumulative_cost': cumulative_cost,
        'gain_loss': gain_loss,
        'realised_pct': gain_loss
    }, ignore_index=True)

    return df
