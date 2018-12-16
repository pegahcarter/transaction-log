from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os.path

hist_prices = pd.read_csv('data/historical/prices.csv')

if not os.path.isfile('data/transactions.db'):
	engine = create_engine('sqlite:///data/transactions.db')
	Base = declarative_base()
	Base.query = db_session.query_property()
	Base.metadata.create_all(bind=engine)
	db_session = scoped_session(sessionmaker(bind=engine))
else:
	engine = create_engine('sqlite:///data/transactions.db')
	db_session = scoped_session(sessionmaker(bind=engine))

