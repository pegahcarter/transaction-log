import pandas as pd

def refresh_df():
	''' update our DataFrame with the recent transactions '''
	engine = create_engine('sqlite:///data/transactions.db')
	df = pd.read_sql_table('transactions', con=engine)
	return df


def add_coin_to_transactions(coin, quantity):
	'''
	Add initial purchase of coin to transactions table

	coin		- coin we're adding
	quantity	- quantity of coin originally purchased
	'''

	current_price = coin_price(coin)
	myTransaction = Transaction(
		coin = coin,
		side = 'buy',
		units = quantity,
		fees = current_price * quantity * 0.00075,
		# previous_units = 0,
		# cumulative_units = quantity,
		transacted_value = current_price * quantity,
		# previous_cost = 0,
		# cost_of_transaction = None,
		# cost_per_unit=None,
		cumulative_cost = current_price * quantity,
		# gain_loss=None,
		# realised_pct=None
	)

	db_session.add(myTransaction)
	db_session.commit()


def update_transactions(coin, side, quantity, dollar_value):
	'''
	Document transaction data to SQL table

	coin 			- coin we're documenting for the trade
	side 			- side we're executing the trade on (buy or sell)
	quantity 		- quantity of coin to be traded
	dollar_value 	- value of our trade in dollars
	'''

	df = refresh_df()
	previous_units, previous_cost = df[df['coin'] == coin][['cumulative_units', 'cumulative_cost']].iloc[-1, :]

	if side == 'buy':
		myTransaction = Transaction(
			coin = coin,
			side = side,
			units = quantity,
			fees = dollar_value * 0.00075,
			previous_units = previous_units,
			cumulative_units = previous_units + quantity,
			transacted_value = dollar_value,
			previous_cost = previous_cost,
			# cost_of_transaction=None,
			# cost_per_unit=None,
			cumulative_cost = previous_cost + dollar_value,
			# gain_loss=None,
			# realised_pct=None
		)
	else:
		myTransaction = Transaction(
			coin = coin,
			side = side,
			units = quantity,
			# fees = None,
			previous_units = previous_units,
			cumulative_units = prev_amt - quantity,
			transacted_value = dollar_value,
			previous_cost = previous_cost,
			cost_of_transaction = quantity / previous_units * previous_cost,
			cost_per_unit = previous_cost / previous_units,
			cumulative_cost = previous_cost - dollar_value,
			gain_loss = dollar_value - cost_of_transaction,
			realised_pct = gain_loss / cost_of_transaction
		)

	db_session.add(myTransaction)
	db_session.commit()
