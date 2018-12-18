from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os.path
#from models import Portfolio
import models
from functions import refresh_df

engine = create_engine('sqlite:///data/transactions.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
	df = refresh_df()

	if len(df) == 0:
		Base.metadata.create_all(bind=engine)
