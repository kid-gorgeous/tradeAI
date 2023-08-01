"""
    This will help manage and understand the risk of the portfolio, the trade, the strategy, market, and outcome. 
    This was taken from a medium article:
        - https://medium.datadriveninvestor.com/calculating-risk-management-statistics-in-python-756ab3cb1851
    A module like this can help assess and mitigate the risk as one of the primary factors that will determine
    the longevity of success and failure. 

    Effective risk management is fundemental to financial success. Understanding the concept of resk and its different
    types is curcial to trading success. Risk refers to the uncertainty or potential for loss associated with the investment
    returns. The three main concept of risk include: Market Risk (deviation of interest rates, econ conditions, geopolitical events),
    Credit Risk (the possibility of default and leveraged based transactions), and Liquidity Risk (the ease of buying and selling w/o
    effecting the price). 

    The key concept of risk management involves identifying and quantifying the risk, and assessing their potential impact
    and implementing strategies to mitigate or manage them effectively. Understanding the different types of risk, investors can
    make informed decisions and design robust investment portoflios. 

"""

# Importing the dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import yfinance as yf
import datetime as dt

# define the requirements 
ticker = 'AAPL'
benchmark_ticker = '^GSPC'
start_date = '2010-01-01'
end_date = '2020-12-31'

# fetch historical price data for the asset and the benchmark
asset_data = yf.download(ticker, start_date, end_date)
benchmark_data = yf.download(benchmark_ticker, start_date, end_date)

# print("\nAsset Data: \n", asset_data)
# print("\nBenchmark Data: \n", benchmark_data)

# Extract the "close" prices from the data
asset_prices = asset_data["Close"]
benchmark_prices = benchmark_data["Close"]

# print("",asset_prices)
# print("",benchmark_prices)

# Calculate the asset returns and benchmark returns
asset_returns = asset_prices.pct_change().dropna()
benchmark_returns = benchmark_prices.pct_change().dropna()

# print("",asset_returns)
# print("",benchmark_returns)

# Calculate the average return
average_return = asset_returns.mean()

# print("",average_return)

# Standard Deviation
standard_deviation = asset_returns.std()
print("Standard Deviation: ",standard_deviation)

# Sharpe Ratio
risk_free_rate = 0.03 # Assume a risk-free rate of 3%
sharpe_ratio = (average_return - risk_free_rate) / standard_deviation
print("Sharpe Ratio: ",sharpe_ratio)

# Sortino Ratio
downside_returns = asset_returns[asset_returns < 0]
average_downside_return = downside_returns.mean()
print("Average Downside Return: ",average_downside_return)
sortino_ratio = (average_return - risk_free_rate) / downside_returns.std()
print("Sortino Ratio: ",sortino_ratio)

# Beta
model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
beta = model.params[1]

# Max Drawdown
cumulative_returns = (asset_returns + 1).cumprod()
# print("Cumulative Returns: ",cumulative_returns)
cumulative_max = cumulative_returns.cummax()
# print("Cumulative Max: ",cumulative_max)
drawdown = (cumulative_max - cumulative_returns) / cumulative_max
# print("Drawdown: ",drawdown)

# Value at Risk (VaR)
confidence_level = 0.95
var = np.percentile(asset_returns, 100-confidence_level * 100)
print("Confidence Level: ",confidence_level)
print("VaR: ",var)

# Conditional Value at Risk (CVaR)
tail_returns = asset_returns[asset_returns < var]
cvar = tail_returns.mean()
print("CVaR: ",cvar)

# R-squared
model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
r_squarded = model.rsquared
print("R-Squared: ",r_squarded)

# Plot 
plt.plot(drawdown)
plt.title("Max Drawdown of {}".format(ticker))
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.show()
max_drawdown = drawdown.max()



