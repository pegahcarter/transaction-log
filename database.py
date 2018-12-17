from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os.path
import datetime
from models import Portfolio, Transaction

hist_prices = pd.read_csv('data/historical/prices.csv')

if os.path.isfile('data/transactions.db'):
	engine = create_engine('sqlite:///data/transactions.db')
	db_session = scoped_session(sessionmaker(bind=engine))
else:
	engine = create_engine('sqlite:///data/transactions.db')
	db_session = scoped_session(sessionmaker(bind=engine))
	Base = declarative_base()
	Base.query = db_session.query_property()
	Base.metadata.create_all(bind=engine)

	# add initial transactions to transactions table
	myPortfolio = Portfolio()
	for i, (quantity, price) in enumerate(zip(myPortfolio.quantities, myPortfolio.current_prices)):
		db_session.add(Transaction(
			date = datetime.datetime.now(),
			coin = myPortfolio.coins[i],
			side = 'buy',
			units = quantity,
			price_per_unit = price,
			fees = price * quantity * 0.00075,
			previous_units = 0,
			cumulative_units = quantity,
			transacted_value = price * quantity,
			previous_cost = 0,
			cost_of_transaction = None,
			cost_per_unit = None,
			cumulative_cost = price * quantity,
			gain_loss = 0,
			realised_pct = None
		))
		db_session.commit()
