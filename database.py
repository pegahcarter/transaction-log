from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os.path
from models import Portfolio

def init_db():
	myPortfolio = Portfolio()
	if os.path.isfile('data/transactions.db'):
		engine = create_engine('sqlite:///data/transactions.db')
		db_session = scoped_session(sessionmaker(bind=engine))
	else:
		engine = create_engine('sqlite:///data/transactions.db')
		db_session = scoped_session(sessionmaker(bind=engine))
		Base = declarative_base()
		Base.query = db_session.query_property()
		Base.metadata.create_all(bind=engine)

	df = pd.read_sql_table('transactions', con=engine)

	for coin, quantity, current_price in zip(myPortfolio.coins, myPortfolio.quantities, myPortfolio.current_prices):
		if coin not in df['coin']:
			add_coin_to_transactions(coin, quantity, current_price)

	return myPortfolio


def refresh_df():
	engine = create_engine('sqlite:///data/transactions.db')
	df = pd.read_sql_table('transactions', con=engine)
	return df
