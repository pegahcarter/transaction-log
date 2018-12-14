import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data/transactions.db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

hist_prices = pd.read_csv('data/historical/prices.csv')

def init_db():
	import models
	Base.metadata.create_all(bind=engine)
