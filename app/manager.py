# this is the "app/manager.py" file

#**************************************************************************
#***************      Importation of Python Libraries             *********
#**************************************************************************
#**************************************************************************

# the following code is for importing some plotting libraries for later use
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'serif'

#
# scipy.optimize is the set of optimization functions that would be useful for portfolio optimization
#
import scipy.optimize as sco

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
#***********    Custom Functions (Modular Program Approach)    ************
#**************************************************************************
#**************************************************************************

def to_Percentage(num):
    '''
        Purpose: To convert some number to a percent. Appends the '%' sign. Outputs a String.
        
        Params: Number of Type Int or Float 
    '''
    newNum = round(num * 100, 2)
    toString = str(newNum) + "%"
    return toString

def negative_sharpe(weights):
    '''
        Purpose: To construct a portfolio which maximizes the Sharpe ratio (or, more precisely, minimizes the negative Sharpe ratio) of a portfolio.

        Params: A numpy array containing portfolio 'weights'.
    '''
    weights = np.array(weights)
    pret = np.dot(weights, mu)
    pvol = np.sqrt(np.dot(weights, np.dot(VarCov, weights.T)))
    return -(pret-rf)/pvol

def minimum_risk(weights):
    '''
        Purpose: To construct a portfolio which minimizes the risk of a portfolio.

        Params: A numpy array containing portfolio 'weights'.
    '''
    weights = np.array(weights)
    pvol = np.sqrt(np.dot(weights, np.dot(VarCov, weights.T)))
    return pvol

def from_CSV(filePath):
    '''
        Purpose: Reads a CSV from a user local drive at a path they have specified.

        Parameters: A string containing complete path to CSV file. Stocks must be indicated 
                    by their ticker within CSV must be under the header 'Ticker'

        Returns: A list variable containing series of stock tickers.
    '''

    #
    # read the stock data, portfolio_stocks.csv, into Python and store it in a variable "stocks"
    #
    stocks = pd.read_csv(filePath)

# creating dictionary with which to store raw company data
    symbols = {}
    index = 0
    for company in stocks["Ticker"]:
        symbols[company] = stocks["Ticker"][index]
        index += 1

    numOfAssets = len(symbols)
    tickers = list(symbols.values())

    return tickers

def stock_upload():
    ''' 
        Purpose: Extracts user ticker information either manually or via CSV upload.

        Parameters: None

        Returns: A list variable containing series of stock tickers.
    '''
    while True:
        uploadForm = input("\nWould you like to provide your current portfolio manually or upload a CSV? Please enter 'manual' or 'upload': ")
        print('\n')
        uploadForm = uploadForm.lower()

        if uploadForm == 'quit':
            print("Exiting program now. Please come back soon! Goodbye...\n")
            quit()
        
        elif uploadForm == 'manual' or uploadForm == 'upload':
            break

        else:
             print("ERROR: Invalid entry. Try again!\n")


    if uploadForm == 'upload':
        print(
            '''
            Note: In order for the CSV to be processed correctly, stocks must be indicated 
                  by their symbol under the header 'Ticker' in the file.
            ''')

        filePath = input("Please specify the file path: ")
        premature_quit(filePath)
        tickers = from_CSV(filePath)

    if uploadForm == 'manual':
        tickers = stock_entry(comparison=False)

    return tickers
    
def premature_quit(str):
    '''
        Purpose: Allows for the user to exit the program by entering 'quit' when prompted for input.

        Params: A string containing user input.
    '''
    if str == 'QUIT' or str == 'quit':
        print("Exiting program now. Please come back soon! Goodbye...\n")
        quit()

def stock_entry(comparison):
        '''
            Purpose: Provides a framework for the manual entry of stock symbols.

            Params: None

            Returns: A list variable containing series of stock tickers.

        '''
        tickers = []
        while True:

            if comparison == True:
                symbol = input("Please enter a stock symbol to evaluate: ")
                symbol = symbol.upper()

            else:
                symbol = input("Please enter stock symbol and enter 'done' when finished: ")
                symbol = symbol.upper()

            premature_quit(symbol)

            if (len(symbol) > 5 or  (symbol.isalpha() == False  and "." not in symbol)): # Stock symbols can contain periods!
                    print("ERROR: Expecting a properly-formed stock symbol like, for example, 'AAPL'.\n")
            
            else:
                if (symbol == "DONE"):
                    if not tickers:
                        emptyListCheck = input("No valid data has been entered. Are you sure? Please enter 'yes' or 'no': ")
                        emptyListCheck = emptyListCheck.upper()

                        while (emptyListCheck != "YES" and emptyListCheck != "NO"):
                            print("\nINVALID  ENTRY! Please try again!")
                            emptyListCheck = input("No valid data has been entered. Are you sure? Please enter 'yes' or 'no': ")
                            emptyListCheck = emptyListCheck.upper()

                        if (emptyListCheck == 'YES'):
                            premature_quit('quit')

                    elif (len(tickers) > 0 ):
                        break

                elif (symbol in tickers):
                    print("\nYou have already entered this symbol!")

                    multipleEntries = input("\nWould you like to enter another stock? Enter 'yes' or 'no': ")
                    multipleEntries = multipleEntries.upper()

                    while (multipleEntries != "YES" and multipleEntries != "NO"):
                        print("\nINVALID  ENTRY! Please try again!")
                        multipleEntries = input("Would you like to enter another stock? Enter 'yes' or 'no': ")
                        multipleEntries = multipleEntries.upper()

                    if (multipleEntries == "NO"):
                        break

                else:
                    tickers.append(symbol)

                if comparison == True:
                    break   
            
        return tickers

def stock_data_retrieval(list):
    '''
        Purpose: Uses the Yahoo! Finance API to fetch historical stock data over a specified period of time.

        Parameters: A list containing stock symbols of companies.

        Returns: A pandas dataframe of historical adjusted close prices for the specified companies.
    '''

    #
    # yf.download function retrieves daily prices for a list of securities in a batch and convert that to a Dataframe
    # here the resulting variable stores the information
    #
    raw = yf.download(list, start = "2016-01-01", end = "2018-12-31")

    # extract the adjusted closing prices and store them in a variable named price_data
    price_data = raw['Adj Close']

    # sort price_data by date in case the price_data was not sorted properly by date
    price_data.sort_index()

    return price_data

def timeframe_selection(price_data):
    '''
        Purpose: Allows the user to specify the intervals with which to construct the returns analysis (daily, monthly, quarterly). Refactors price data accordingly.

        Params: A pandas variable 'price_data' containing historical prices.

        Returns: A string variable 'timing' which is incorprated into the analysis.
    '''

    attempts = 0
    while attempts < 4:
        timingChoice = input("\nConstruct portfolio using daily, monthly, or quarterly: ")
        timingChoice = timingChoice.lower()

        byDay = ["daily", "day", "d"]
        byMonth = ["monthly", "month", "m"]
        byQuarter = ["quarterly", "quarter", "q"]

        if timingChoice in byDay:
            timing = 252
            break
        elif timingChoice in byMonth:
            timing = 12
            price_data = price_data.resample(rule = 'm', label = 'right').last()
            break
        elif timingChoice in byQuarter:
            timing = 4
            price_data = price_data.resample(rule = 'q', label = 'right').last()
            break
        else:
            print("\nERROR: Invalid Entry. Please enter 'daily', 'monthly', or 'quarterly': ")
        attempts += 1

        if (attempts == 4):
            print("\nMaximum Attempts Reached: Defaulting to daily returns.")
            timing = 252
            break

    return timing

def fetch_returns(price_data):
    '''
        Purpose: To calculate historical stock returns.

        Params: A pandas datframe containing historical returns and a 'timing' variable to determine return period

        Returns: A pandas variable contain stock returns. 
    '''

    #
    # generate log-returns or continuously compounded returns for all securities and store them in dataframe "rets"
    rets = np.log(price_data / price_data.shift(1))

    return rets

def fetch_RiskFreeRate():
    '''
        Purpose: Dynamically setting the risk-free rate. To be used in portfolio construction.

        Params: None

        Returns: The Risk Free Rate.
    '''

    riskFree = yf.download("^IRX", start = "2015-01-01", end = "2018-12-31")
    rf_prices = riskFree["Adj Close"]
    averageRF = rf_prices.mean()
    rf = averageRF/100

    return rf


if __name__ == "__main__":

    #**************************************************************************
    #***************                  Module 1                      ***********
    #********************  Introduction to the Application  *******************
    #**************************************************************************

    #Welcome Message
    print("\n\nWelcome to Planalytics LLC. Securities Manangement Software!")
    print(
    '''
The following program will recieve stock data via CSV upload or manual
entry (ex. IBM, AAPL, MSFT) and produce various portfoio analysis on that data.

The historical data (from the previous three years) will be used to conduct techincal
analysis on each stock entered, as well as on entire portfolios.

Please be sure to provide accurate stock symbols to avoid receiving an error messages.

-——————————————————————————————————————————————————————————————————————————————
If at any point you wish to exit the program prematurely, please enter 'quit'.
\n''')

    #**************************************************************************
    #***********                       Module 2                       *********
    #***************       Data Retrieval of User Preferences   ***************
    #**************************************************************************

    #Investment Approach
    print(

        ''' This software offers a number of approaches for portfolio management. Which of the following do you prefer:

            Integrative: Enter equities you already own to recieve feedback on balancing your portfolio among these stocks.

            Speculative: Enter stocks you are interested in to recieve Buy, Sell, Hold recommendations.

            Holistic: Enter stocks within your current portfolio. After doing so, you may enter new stocks to recieve their impact on your portfolio.
    ''')

    ifIntegrative = ['integrative', 'int', 'i']
    ifSpeculative = ['speculative', 'spec', 's']
    ifHolistic = ['holistic', 'hol', 'h']
    status = False

    while True:

        invApproach = input("Please enter 'Integrative', 'Speculative' or 'Holistic': ")
        invApproach = invApproach.lower()

        premature_quit(invApproach)

        if invApproach in ifHolistic:
            invApproach = 'holistic'
            status = True

        if invApproach in ifIntegrative:
            invApproach = 'integrative'
            status = True

        if invApproach in ifSpeculative:
            invApproach = 'speculative'
            status = True

        if status == True:
            confirmation = f"\nYou have selected the {invApproach} approach."
            print(confirmation)
            break

        print("ERROR: Invalid entry. Try again!\n")

    # Investor Risk Tolerance
    print(f'''

                                                        INVESTMENT STRATEGY


            In order for us to determine an investment strategy for the {invApproach} approach, we must first know your risk tolerance.

                    Aggressive: Maximizing returns by taking a high degree of risk. This strategy will focus on capital appreciation
                                by recommending the purchase of what are commonly know as "high-growth" stocks and the liquidation of stocks
                                with low growth opportunity.


                    Moderate:   This strategy attempts to find a balance between aggressive and conservative strategies by suggesting
                                allocation toward so-called "value" stocks. These stocks have moderate growth potential and
                                are typically undervalued by the market. Returns on this strategy are fairly volatile in the short-term
                                but are favorable in the long-term


                Conservative:   Maximizing the safety of the principal investment by accepting little-to-zero risk. This strategy will
                                suggest allocation to "sturdy" stocks - i.e. companies with a history of stable cash flows. Returns are
                                considerably lower under this strategy.

            ''')

    ifAggressive = ['aggressive', 'a']
    ifModerate = ['moderate', 'm']
    ifConservative = ['conservative', 'c']
    status = False

    while True:
        risk_tolerance = input("Please select an investment strategy. Enter 'Aggressive', 'Moderate, or 'Conservative': ")
        risk_tolerance = risk_tolerance.lower()

        premature_quit(risk_tolerance)

        if risk_tolerance in ifAggressive:
            risk_tolerance = 'aggressive'
            status = True

        if risk_tolerance in ifModerate:
            risk_tolerance = 'moderate'
            status = True

        if risk_tolerance in ifConservative:
            risk_tolerance = 'conservative'
            status = True

        if status == True:
            confirmation = f"\nYou have selected the {risk_tolerance} investment strategy."
            print(confirmation)
            break

        print("ERROR: Invalid entry. Try again!\n")


    #**************************************************************************
    #***********                       Module 3                       *********
    #***************    Portfolio Construction and Recommendations   **********
    #**************************************************************************

    if invApproach == 'integrative':

        comparison = False

        print( 
            '''
                Which of the following portfolios do you wish to construct:

                  1.  Minimum Risk: Your portfolio will be rebalanced based upon the risk tolerance you've indicated.

                  2.  Maximizing Risk-Return Profile: This portfolio will provide the greatest level of return per-unit of risk.
            '''
        )

        while True:
            portfolioSelection = input("Select one of the above portfolio constructions. Enter '1', or '2': ")

            premature_quit(portfolioSelection)

            if portfolioSelection != '1' and portfolioSelection != '2':
                print("\nINVALID  ENTRY! Please try again!")
            else:
                break


        tickers = stock_upload()
        price_data = stock_data_retrieval(tickers)
        rets = fetch_returns(price_data)
        timing = timeframe_selection(price_data)
        mu = rets.mean() * timing
        VarCov = rets.cov() * timing
        rf = fetch_RiskFreeRate()

        if portfolioSelection == '1':

            numOfAssets = len(rets.keys())

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
            opt_mve = sco.minimize(minimum_risk, initial_guess, bounds=bnds, constraints=cons)

            #
            # to extract the optimal portfolio weights, call it through 'x'
            #
            mve_weights = opt_mve['x']

            sharpeRatio = -negative_sharpe(mve_weights)
            sharpeRatio = round(sharpeRatio, 2)

            print("---------------------------------------------------------\n")

            print("OPTIMAL PORTFOLIO CONSTRUCTION FOR MINIMUM RISK:\n")

            index = 0
            stockWeights = {}
            for stock in tickers:
                stockWeights[tickers[index]] = to_Percentage(mve_weights[index])
                index += 1

            for item in stockWeights:
                stockWeights[item] = float(stockWeights[item].replace('%', ""))
                if stockWeights[item] > 0:
                    print(item.rjust(8), "  ", str(stockWeights[item]) + "%")

            print("\n---------------------------------------------------------\n")


        if portfolioSelection == '2':


            numOfAssets = len(rets.keys())

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

            sharpeRatio = -negative_sharpe(mve_weights)
            sharpeRatio = round(sharpeRatio, 2)

            print("---------------------------------------------------------\n")

            print("OPTIMAL PORTFOLIO CONSTRUCTION FOR MAXIMUM RISK-RETURN:\n")

            index = 0
            stockWeights = {}
            for stock in tickers:
                stockWeights[tickers[index]] = to_Percentage(mve_weights[index])
                index += 1

            for item in stockWeights:
                stockWeights[item] = float(stockWeights[item].replace('%', ""))
                if stockWeights[item] > 0:
                    print(item.rjust(8), "  ", str(stockWeights[item]) + "%")

            print("\n---------------------------------------------------------\n")


    if invApproach == 'speculative':

        comparison = False
        tickers = stock_upload()
        price_data = stock_data_retrieval(tickers)
        rets = fetch_returns(price_data)
        validTickers = list(rets.keys())
        mu = rets.mean() * 252

    
        for stock in validTickers:

           # Recommendation
           rec = ""
           reason = ""

           if (risk_tolerance == 'aggressive'):
           
               if (mu[stock].mean() >= 0.08):
                   rec = "BUY"
                   reason = ''' The stock is demonstrating upward momentum. 
                            Asset offers a high-growth proposition.'''

               elif (mu[stock] <= 0.04):
                   rec = "SELL"
                   reason = ''' The stock is demonstrating low growth value, 
                            currently generating less than 4% annual return 
                            An aggressive strategy calls for the liquidation 
                            of low-growth postions.'''
               else:
                   rec = "HOLD"
                   reason = ''' The stock is generating resonable returns
                            and should be held until its growth proposition 
                            is more clear to the market.'''

           elif (risk_tolerance == 'moderate'):

               if (mu[stock].mean() >= 0.06):
                   rec = "BUY"
                   reason = ''' The stock is currently generating greater than 6% annual 
                            return offering relatively strong growth value to an 
                            investor willing to incur moderate risk.'''

               elif (mu[stock] <= 0.03):
                   rec = "SELL"
                   reason = ''' The stock is generating less than 3% annual return, 
                            indicating that the market recognizes little growth value 
                            in the stock moving forward.'''           
               else:
                   rec = "HOLD"
                   reason =''' The stock is generating resonable returns
                            and should be held until its growth proposition 
                            is more clear to the market.'''
           else:

               if (mu[stock] >= 0.01):
                   rec = "BUY"
                   reason = ''' The stock is generating moderate returns. 
                            A conservative strategy focuses on principal 
                            protection rather than growth.'''

               elif (mu[stock] <= -0.01):
                   rec = "SELL"
                   reason = ''' The stock is currently generating negative
                            annual returns, indicating that principal is 
                            at risk. Conservative investors should sell.'''
               else:
                   rec = "HOLD"
                   reason = ''' The stock is demonstrating relative stability, 
                            offering predictability and consistent 
                            returns to conservative investors. '''

           print("\n-----------------------------------------------------------------------------------")
           print(f"SELECTED SYMBOL: {stock.upper()}")
           print(f"RISK TOLERANCE: {risk_tolerance.upper()}")
           print("-----------------------------------------------------------------------------------")
           print(f"AVERAGE ANNUAL RETURN (3-YEAR SAMPLE): {to_Percentage(float(mu[stock]))}")
           print("-----------------------------------------------------------------------------------")
           print(f"RECOMMENDATION: {rec}")
           print(f"RECOMMENDATION REASON: {reason}")
           print("-----------------------------------------------------------------------------------")        


    if invApproach == 'holistic':

        print("Please provide the stocks currently contained within your portfolio.")
        tickers = stock_upload()
        price_data = stock_data_retrieval(tickers)
        rets = fetch_returns(price_data)
        mu = rets.mean() * 252
        VarCov = rets.cov() * 252
        rf = fetch_RiskFreeRate()
    
        #assuming portfolio is well-diversified
        numOfAssets = len(rets.keys())

        #
        # assuming equal weighted portfolio to reduce complexity
        #
        weights = [1/numOfAssets for x in range(numOfAssets)]

        sharpeRatio = -negative_sharpe(weights)
        sharpeRatio = round(sharpeRatio, 2)

        print("\nNow provide a stock you'd like to consider purchasing.")
        comparison = True
        newStock = stock_entry(comparison)
        new_price_data = stock_data_retrieval(newStock)
        new_rets = fetch_returns(new_price_data)
        new_mu = new_rets.mean() * 252

        if len(newStock) == 1:
            new_VarCov = np.var(new_rets) * 252
        else:
            new_VarCov = new_rets.cov() * 252

        new_numOfAssets = len(newStock)
        new_weights = [1/new_numOfAssets for x in range(new_numOfAssets)]
        new_weights = np.array(new_weights)
        new_pret = np.dot(new_weights, new_mu)
        new_pvol = np.sqrt(np.dot(new_weights, np.dot(new_VarCov, new_weights.T)))
        newSharpe = (new_pret-rf)/new_pvol
        newSharpe = float(newSharpe)
        newSharpe = round(newSharpe, 2)

        rets = rets.mean(axis=1)

        while len(rets) > len(new_rets):
            rets.drop(rets.tail(1).index,inplace=True)


        rets.drop(rets.head(1).index,inplace=True)
        new_rets.drop(new_rets.head(1).index,inplace=True)


        corrcoef = np.corrcoef(new_rets, rets)
        corr = corrcoef.sum(axis=0)
        corr = list(corr)
        correlation = corr[0]-1

        print("---------------------------------------------------------\n")
        print("\nRESULT:")

        if (newSharpe >= (sharpeRatio * correlation) ):
            print('''
    This stock improves the risk-return profile of your portfolio. 
    You should include it within your portfolio.

            ''')


        else:
            print('''
    This stock DOES NOT improve the risk-return profile of your portfolio. 
    You should NOT include it within your portfolio.
            ''')

        print("---------------------------------------------------------\n")