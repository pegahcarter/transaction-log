import datetime
import pandas as pd
import numpy as np
import models
import exchange

file = '../data/portfolio/transactions.csv'

def create():
    ''' Create our transactions CSV file if it doesn't yet exist '''

    myPortfolio = models.Portfolio()
    try:
        df = pd.read_csv(file)
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
            df = add_coin(coin, myPortfolio, df)

	if new_transaction(df):
		df.to_csv(file)

    return df


def new_transaction(df):
	if len(df) > len(pd.read_csv(file)):
		return True


def add_coin(coin, myPortfolio, df, date=None):
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
    units 			- units of coin to be traded
    dollar_value    - value of our trade in dollars
    df              - transactions dataframe
    '''

	prev_units = df[df['coin'] == coin]['cumulative_units'].iloc[-1]
	prev_cost = df[df['coin'] == coin]['cumulative_cost'].iloc[-1]

    if date is None:
        date = datetime.datetime.now()
        current_price = exchange.price(coin)

    if side == 'buy':
        fees = dollar_value * 0.00075
        cumulative_units = prev_units + units
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
