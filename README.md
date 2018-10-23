# rebalance-my-portfolio
Want to automatically rebalance your personal cryptocurrency portfolio?  This
repository ensures that your cryptocurrencies maintain an equal dollar value
AND documents every transaction into a SQL database.


## Steps to setup
1. Download/clone this repository to your local computer
2. Modify api.txt with your personal API key and secret
3. Install [Python 3](https://www.python.org/downloads/)
	- Packages to `pip install`: numpy, pandas, ccxt, sqlalchemy
4. If you are using an exchange other than Binance:
	- Within rebalance.py, edit line 30 with your exchange name
5. Schedule rebalance frequency
	- Windows:
		- windows search `Task Scheduler`
		- select `Create Task`
		- select the `Triggers` tab, and set the interval for the program to run
		- select the Actions tab, and click `New...`
		- For `Program/Script`, insert your python.exe location (e.g. `C:\Users\Carter\AppData\Local\Python\python.exe`)
		- For `Add arguments (optional)`, insert your rebalance.py location (e.g. `C:\Users\Carter\Documents\rebalance-my-portfolio\rebalance.py`)
		- Done!
	- Mac:
		- good luck!
