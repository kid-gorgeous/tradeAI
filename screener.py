"""
    https://towardsdatascience.com/making-a-stock-screener-with-python-4f591b198261

    Example Criteria:
        - the current price of the security must be greater than the 150 and 
        200 day simple moving average
        - the 150 day simple moving average must be greater than the 200 day 
        simple moving average
        - the 200-day simple moving average must be trending up for at least 1 month
        - the 50-day simple moving average must be greater than the 150 simple
        moving average and the 200 simple moving average
        - the current price must be greater than the 50-day simple moving average
        - the current price must be at least 30% above the 52 week low
        - The current price must be within 25% of the 52 week high
        - the IBD RS rating must be greater than 70 (the higher is better) 

"""

""" TODO:
    Optimize the code to run faster, and more efficiently by creating an excusable time frame for the data to be pulled allowing for the program to only run once or twice a day.
"""

from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter

import yfinance as yf
import pandas as pd
import datetime
import time
yf.pdr_override()

# this will yoink the ticker symbols from the sp500
tickers = si.tickers_sp500()
tickers = [item.replace(".", "-") for item in tickers] # Yahoo Finance uses dashes instead of dots

print(tickers)

# index name, start, and end time
index_name = 'NVDA' # S&P 500
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = datetime.date.today()


# exportList of index information
exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
returns_multiples = []

# index returns
index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
index_df['Precent Change'] = index_df['Adj Close'].pct_change()
index_return = (index_df['Precent Change'] + 1).cumprod()[-1]

for ticker in tickers:
    # download historical data as CSV for each stock
    df = pdr.get_data_yahoo(ticker, start_date, end_date)
    df.to_csv(f'./symbols/{ticker}.csv')

    # calculate returns relative to the market
    df['Percent Change'] = df['Adj Close'].pct_change()
    stock_return = (df['Percent Change'] + 1).cumprod()[-1]

    returns_multiple = round((stock_return / index_return), 2)
    returns_multiples.extend([returns_multiple])

    print (f'Ticker: {ticker}; Returns Multiple against S&P 500: {returns_multiple}\n')
    time.sleep(1) # unnecessary but will help curb potential errors... (working on fix for next week... TODO)

# dataframe of stocks and their returns
rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]

"""
    As per a tutorial...

    Next the cumulative return of the S&P 500 index over the past year and compare that value to the cumulative return
    of for each stock in the list during the same period of time. 

    The IBD Relative Strength metric essentially calculates how a stock is performing relative to the market and other
    stocks at that time. The IBD RS can help estimate a percentile ranking for each of the stock out of 100 marks. 
         - By dividing the cumulative return of each stock over the cumulative return of the index and then ranking.

    For example, AAPL outperformed the market greater than MSFT in a specified time period, it would have a higher RS.
    In Mark Minervini's Trend Template, the formula will help select stocks that have a higher RS score. The top 30% of
    the best performing stocks are selected.
    
    This can handle up to ~500 stocks in the S&P index. 

    Finally, after the data manipulation with quantiles, a dataframe is created with the top 30% performing stocks in a
    given list with their respective RS scores.
"""

# checking minervini conditions of top 30% of stocks in the list
rs_stocks = rs_df["Ticker"]
for stock in rs_stocks:
    try:
        # altered line of code to access a file system of indexed stocks
        df = pd.read_csv(f'./symbols/{stock}.csv', index_col=0)
        sma = [50, 150, 200]
        for x in sma:
            # calculates the sma over a series of rolling windows based on the mean of the adjusted close to 2 decimal places
            df["SMA_"+str(x)] = round(df['Adj Close'].rolling(window=x).mean(),2)

        # stored values based on the current day (last value in the list)
        currentClose = df["Adj Close"][-1]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        # the list comphrension is used to get the last 260 days of data, and then the min value is found 
        # (the lowest price over the last year)
        low_of_52week = round(min(df["Low"][-260:]), 2)
        # the same type of list comprehension is used again but for the max value (the highest price over the last year)
        high_of_52week = round(max(df["High"][-260:]), 2)
        # the following comprehension is based on the current Ticker stock symbol, and the RS rating found from the
        # first item in the columns stack
        RS_Rating = round(rs_df[rs_df['Ticker']==stock].RS_Rating.tolist()[0])

        try: # taking the last 20 days of data and finding the moving average
            moving_average_200_20 = df["SMA_200"][-20]
            # thank you github coplit lmao
        except Exception:
            moving_average_200_20 = 0

        # the next part defines the conditions for the minervini strategy
        
        # So, ... Condition 1: Current Prive >? 150 SMA and >? 200 SMA
        # nice bound checking lmfaoooo
        condition_1 = currentClose > moving_average_150 > moving_average_200

        # Condition 2: 150 SMA and >? 200 SMA
        condition_2 = moving_average_150 > moving_average_200

        # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        condition_3 = moving_average_200 > moving_average_200_20

        # Condition 4: 50 SMA > 150 SMA and 50 SMA > 200 SMA
        condition_4 = moving_average_50 > moving_average_150 > moving_average_200
        # thank you github coplit lmao

        # Condition 5: Current Price > 50 SMA
        condition_5 = currentClose > moving_average_50

        # Condtion 6: Current Prive is at least 30% above 52 week low
        condition_6 = currentClose >= (1.3 * low_of_52week)

        # Condition 7: Current Prive is within 25% of 52 week high
        condition_7 = currentClose >= (.75 * high_of_52week)

        # if all the conditions above are true, add the acquired stock to the exportList
        if (condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7):

            # this line marked for depreciation
            exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50,
                                            "150 Day MA": moving_average_150, "200 Day MA": moving_average_200,
                                            "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
            print (stock + " made the Minervini requirements")

    except Exception as e:
        print(e)
        print(f"Could not gather data on {stock}")

exportList = exportList.sort_values(by='RS_Rating', ascending=False)


# YOOOOO AND IT WRITES TO EXCEL BOI
writer = ExcelWriter("ScreenOutput.xlsx")
exportList.to_excel(writer, "Sheet1")
writer.save() # this line marked for depreciation


"""
    By calculating the metrics for each one of the stocks, we can just include the top 30% of the stocks in the list that pass condition 8 of the Minervini's Trend Template ( an RS value greater than 70). Next, the metric conditioned by the close price and the adjusted price of the last day, the highs and lows of the past year are taken into account. The minimum and maximum values in the DataFrame for the past 260 trading days. 

    The moving averages are used by calculating the rolling averages over the respective amount of days. 

    The code will print a DataFrame of all the stocks that made the requirements and download the stocks to an Excel file. 

"""