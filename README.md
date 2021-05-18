# Portfolio-Management
Robo-Advisor utilizing user preferences, risk tolerance, and varying investment approaches to produce portfolio management recommendations and advice for the user. [GitHub Repo](https://github.com/antoniogriffith/Portfolio-Management).


# Prerequisites
* Command-Line Application (Terminal or Git Bash)
* Python Installation (3.7+)

# Custom Functions
* to_Percentage
```
        Purpose: To convert some number to a percent. Appends the '%' sign. Outputs a String.
        
        Params: Number of Type Int or Float 
```
* negative_sharpe
```
        Purpose: To construct a portfolio which maximizes the Sharpe ratio (or, more precisely, minimizes the negative Sharpe ratio) of a portfolio.

        Params: A numpy array containing portfolio 'weights'.
```
* minimum_risk
```
        Purpose: To construct a portfolio which minimizes the risk of a portfolio.

        Params: A numpy array containing portfolio 'weights'.
```
* from_CSV
```
        Purpose: Reads a CSV from a user local drive at a path they have specified.

        Parameters: A string containing complete path to CSV file. Stocks must be indicated 
                    by their ticker within CSV must be under the header 'Ticker'

        Returns: A list variable containing series of stock tickers.
```
* stock_upload
``` 
        Purpose: Extracts user ticker information either manually or via CSV upload.

        Parameters: None

        Returns: A list variable containing series of stock tickers.
```
* premature_quit
```
        Purpose: Allows for the user to exit the program by entering 'quit' when prompted for input.

        Params: A string containing user input.
```
* stock_entry
```
        Purpose: Provides a framework for the manual entry of stock symbols.

        Params: None

        Returns: A list variable containing series of stock tickers.
```
* stock_data_retrieval
```
    Purpose: Uses the Yahoo! Finance API to fetch historical stock data over a specified period of time.

    Parameters: A list containing stock symbols of companies.

    Returns: A pandas dataframe of historical adjusted close prices for the specified companies.
```
* timeframe_selection
```
    Purpose: Allows the user to specify the intervals with which to construct the returns analysis (daily, monthly, quarterly). Refactors price data accordingly.

    Params: A pandas variable 'price_data' containing historical prices.

    Returns: A string variable 'timing' which is incorprated into the analysis.
```
* fetch_return
```
    Purpose: To calculate historical stock returns.

    Params: A pandas datframe containing historical returns and a 'timing' variable to determine return period

    Returns: A pandas variable contain stock returns. 
```
* fetch_RiskFreeRate
```
    Purpose: Dynamically setting the risk-free rate. To be used in portfolio construction.

    Params: None

    Returns: The Risk Free Rate.
```


# Setup

Create and activate a new virtual environment:

```sh
conda create -n stockmanager-env python=3.8
conda activate stockmanager-env
```

Copy the default stock information (then customize the resulting "default_stocks.csv" file with your own portfolio stocks as desired):

```sh
cp data/default_stock.csv
```

## Installation

Install package dependencies:

```sh
pip install -r requirements.txt
```

# Usage 

## Step 1: Run the program: - the specific run abbreviated command is as follows:

```sh
python -m app.manager
```

## Step 2: User input will be asked to enter specific preference,including investment strategy and risk tolerance.

## Step 3: User selects a specific technical analysis to be produced: integrative, speculative, holistic.

```sh
Integrative: Enter equities you already own to recieve feedback on balancing your portfolio among these stocks.

Speculative: Enter stocks you are may like to recieve Buy, Sell, Hold recommendations for.

Holistic: Enter stocks within your current portfolio. After doing so, you may enter new stocks to recieve their impact on your portfolio.
```

#### These instrutions can also be found within the program.


## Step 4: User is able to provide as many stocks as required either via manual entry or CSV upload.

### If CSV upload, the file should follow the following format:
```sh
id,Company Name,Ticker,Sector
1,"Apple, Inc.",AAPL,TECHNOLOGY
2,"Facebook, Inc.",FB,TECHNOLOGY
3,Microsoft Corp.,MSFT,TECHNOLOGY
4,"Netflix, Inc.",NFLX,TECHNOLOGY
5,"Paypal, Inc.",PYPL,TECHNOLOGY
```

## Step 5: Program produces advise/recommendations specific to the user's preferences.


## Step 6: Program will then exit automatically.


To use the program again, repeat Step 1


## Testing

Running all tests:

```sh
pytest
```