# this is the "app/manager.py" file


#**************************************************************************
#***************                  BLOCK 1                      ************
#**************************************************************************
#**************************************************************************

# the following code is for importing some plotting libraries for later use
#
from pylab import plt
plt.style.use('ggplot')
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'serif'

#
# scipy.optimize is the set of optimization functions that would be useful for portfolio optimization
#
import scipy.optimize as sco

#
# now we import numpy and pandas libraries
# numpy is going to be very helpful when we deal with a large number of assets through vector/matrix algebra
import numpy as np
import pandas as pd
#
# pd.options.display customizes the display options for datasets
#
pd.options.display.max_seq_items = 10
pd.options.display.max_rows = 10

#
# yfinance is a third party package that allows downloading some data from Yahoo Finance firectly;
# you need to install this package first before you are able to use the functions inside this package
# 
import yfinance as yf

#**************************************************************************
#***************                  BLOCK 2                       ***********
#**************************************************************************
#**************************************************************************

#
# read the stock data, portfolio_stocks.csv, into Python and store it in a variable "stocks"
#
stocks = pd.read_csv("/Users/antoniogriffith-keaton/Documents/GU Docs/FINC 241/Group Project/Data/portfolio_stocks.csv")

# creating dictionary with which to store raw company data
symbols = {}
index = 0
for company in stocks["Company Name"]:
    symbols[company] = stocks["Ticker"][index]
    index += 1

numOfAssets = len(symbols)
tickers = list(symbols.values())

#
# yf.download function retrieves daily prices for a list of securities in a batch and convert that to a Dataframe
# here the resulting variable stores the information
#
raw = yf.download(tickers, start = "2014-01-01", end = "2018-12-31")

# extract the adjusted closing prices and store them in a variable named price_data
price_data = raw['Adj Close']

# sort price_data by date in case the price_data was not sorted properly by date
price_data.sort_index()

#
# generate log-returns or continuously compounded returns for all securities and store them in dataframe "rets"
# we use the "shift" method in the calculation
# then we preview the "rets"
#
rets = np.log(price_data / price_data.shift(1))

# Plot the individual securities' returns in the sample period
rets.cumsum().plot(figsize=(30,15))

#**************************************************************************
#***************                 BLOCK 3                       ************
#**************************************************************************
#**************************************************************************

#
# from daily return to annual return, multiply the daily return by 252
# from monthly to annaul, multiply monthly by 12
# from quarterly to annual, multuply quarterly by 4
#
mu = rets.mean() * 52

#
# from daily variance-covariance to annuak variance-covariance, multiply the daily version by 252
# from monthly to annual, multiply by 12
# from quarterly to annual, multiply quarterly by 4
#
VarCov = rets.cov() * 52

#
# pre-set the risk-free rate to be 1% per year and store it in the variable "rf"
#
rf = 0.01


#**************************************************************************
#***************                 BLOCK 4                       ************
#**************************************************************************
#**************************************************************************

#
# define a function that returns the negative Sharpe ratio if you pass the portfolio weights to the function
#
def negative_sharpe(weights):
    weights = np.array(weights)
    pret = np.dot(weights, mu)
    pvol = np.sqrt(np.dot(weights, np.dot(VarCov, weights.T)))
    return -(pret-rf)/pvol

#
# initial guess for the portfolio weights. Typically we start with equal weights as an initial guess
#
initial_guess = [1/numOfAssets for x in range(numOfAssets)]

#
# portfolio constraint: summation of weights should be 1
#
cons = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

#
# impose additional constraint: does not allow short sale, i.e. all the individual weights between 0 and 1
#
bnds = tuple((0,1) for x in range(numOfAssets))

#
# now we are ready to use the minimization function
# if you are leaving the arguments to "none", then you don't need to include them
#
opt_mve = sco.minimize(negative_sharpe, initial_guess, bounds=bnds, constraints=cons)

#
# to extract the optimal portfolio weights, call it through 'x'
#
mve_weights = opt_mve['x']

sharpeRatio = negative_sharpe(mve_weights)*-1

print("\nSharpe Ratio: ", sharpeRatio, "\n")


def to_Percentage(num):
    '''
        Params: Number in Decimal Format
    '''
    newNum = round(num * 100, 2)
    toString = str(newNum) + "%"
    return toString

index = 0
stockWeights = {}
for stock in tickers:
    stockWeights[tickers[index]] = to_Percentage(mve_weights[index])
    index += 1

for item in stockWeights:
    stockWeights[item] = float(stockWeights[item].replace('%', ""))
    if stockWeights[item] > 0:
        print(item.rjust(8), "  ", str(stockWeights[item]) + "%")


sum = 0
for item in stockWeights:
    weightsToAdd = stockWeights[item]
    sum += weightsToAdd
print("\nThe sum of the individual security weights in the portfolio is ", sum)

#
# calculate the MVE portfolio's expected return
#
mve_ret = np.dot(mve_weights, mu)
print("\nThe MVE portfolio's expected return is ", to_Percentage(mve_ret))


#
# calculate the return volatility for the MVE portfolio
#
mve_vol = np.sqrt(np.dot(mve_weights, np.dot(VarCov, mve_weights.T)))
print("\nThe MVE portfolio's expected volatility is ", to_Percentage(mve_vol))

#
# Sharpe Ratio for individual securities
#

print("\nThe Sharpe Ratio for the individual securities is as follows:\n\n")
print((rets.mean()*252-rf)/(np.sqrt(252)*rets.std()))

# plots the MVE portfolio's returns over the sample period
pd.DataFrame(np.dot(rets, mve_weights), columns = ['MVE Portfolio Return'], index = rets.index).cumsum().plot(figsize = (30,15))

pd.DataFrame(np.dot(rets,mve_weights), columns = ['MVE Portfolio Return'], index = rets.index).dropna().mean()*252