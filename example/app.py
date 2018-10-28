from templates.setup import Base, Transactions
from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

engine = create_engine('sqlite:///data/transactions.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
query = ''' SELECT * FROM transactions'''
transactions = pd.read_sql(sql=query, con=engine)
coins = list(set(transactions['coin'].tolist()))
data = json.dumps(coins)


@app.route('/')
def showData():
	return render_template('index.html', data=data)

if __name__ == "__main__":
	app.run(debug=True)
