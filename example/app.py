from templates.setup import Base, Transactions
from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random
import string
import httplib2
import json
import requests
import numpy as np
import pandas as pd
import plotly
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


engine = create_engine('sqlite:///data/transactions.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

DBSession = sessionmaker(bind=engine)
session = DBSession()
query = ''' SELECT * FROM transactions'''

@app.route('/')
def showData():
	transactions = Transactions.query.all()
	return render_template('index.html', transactions=transactions)


if __name__ == "__main__":
	app.run(debug=True)
