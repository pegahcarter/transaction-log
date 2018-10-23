import os
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transactions(Base):
	__tablename__ = 'transactions'

	trade_num = Column(Integer, primary_key=True)
	rebalance_num = Column(Integer)
	date = Column(DateTime, default=datetime.datetime.utcnow)
	coin = Column(String(10))
	side = Column(String(10))
	units = Column(Float(10,2))
	price_per_unit = Column(Float(10,2))
	fees = Column(Float(10,2))
	previous_units = Column(Float(10,2))
	cumulative_units = Column(Float(10,2))
	transacted_value = Column(Float(10,2))
	previous_cost = Column(Float(10,2))
	cost_of_transaction = Column(Float(10,2))
	cost_per_unit = Column(Float(10,2))
	cumulative_cost = Column(Float(10,2))
	gain_loss = Column(Float(10,2))
	realised_pct = Column(Float(10,2))


# Create an engine that stores the database within our sql folder
db = 'sql/transactions.db'
engine = create_engine('sqlite:///' + db)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
