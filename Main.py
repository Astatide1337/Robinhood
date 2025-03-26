import robin_stocks.robinhood as r 

'''
This is an example script that will show you how to check the performance of your open positions.
'''

#!!! Fill out username and password
username = ''
password = ''
#!!!

login = r.login(username, password)

# Query your positions
positions = r.get_open_stock_positions()

# Get Ticker symbols
tickers = [r.get_symbol_by_url(item["instrument"]) for item in positions]

# Get your quantities
quantities = [float(item["quantity"]) for item in positions]

# Query previous close price for each stock ticker
prevClose = r.get_quotes(tickers, "previous_close")

# Query last trading price for each stock ticker
lastPrice = r.get_quotes(tickers, "last_trade_price")

# Calculate the profit per share
profitPerShare = [float(lastPrice[i]) - float(prevClose[i]) for i in range(len(tickers))]

# Calculate the percent change for each stock ticker
percentChange = [ 100.0 * profitPerShare[i] / float(prevClose[i]) for i in range(len(tickers)) ]

# Calcualte your profit for each stock ticker
profit = [profitPerShare[i] * quantities[i] for i in range(len(tickers))]

# Combine into list of lists, for sorting
tickersPerf = list(zip(profit, percentChange, tickers))

tickersPerf.sort(reverse=True)

print ("My Positions Performance:")
print ("Ticker | DailyGain | PercentChange")
for item in tickersPerf:
  print ("%s %f$ %f%%" % (item[2], item[0], item[1]))

print ("Net Gain:", sum(profit))

r.logout()



"""
How to not get banned from Robinhood API:
Docs: https://robin-stocks.readthedocs.io/en/latest/

A fixed interval would be easy to detect on their end.
worried about timing of requests? generate a bimodal Gaussian distribution for waiting times.
from random import gauss, random
from time import sleep

s = random()
if s < 0.3:
    t = gauss(10, 2)
else:
    t = gauss(30, 5)
t = max(min(t,120),5)
sleep(t)

You can get crazier than this and sample from multiple distributions or look into research on user behavior to try and best mimic a user. I knew a guy who wrote his own mouse driver with laplacian curves to mimic a user and avoid detection.
"""