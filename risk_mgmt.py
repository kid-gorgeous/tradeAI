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


class RiskAnalysis:
    def __init__(self, ticker, benchmark_ticker, start_date, end_date, risk_free_rate):
        self.ticker = ticker
        self.benchmark_ticker = benchmark_ticker
        self.start_date = start_date
        self.end_date = end_date
        self.risk_free_rate = risk_free_rate

    def getHistoricalData(self, ticker, start_date, end_date):
        asset_data = yf.download(ticker, start_date, end_date)
        return asset_data

    def getBenchmarkData(self, benchmark_ticker, start_date, end_date):
        benchmark_data = yf.download(benchmark_ticker, start_date, end_date)
        return benchmark_data

    def getReturns(self, asset_data, benchmark_data):
        asset_returns = asset_data["Close"].pct_change().dropna()
        benchmark_returns = benchmark_data["Close"].pct_change().dropna()
        return asset_returns, benchmark_returns

    def getAverageReturn(self, asset_returns):
        average_return = asset_returns.mean()
        return average_return

    def getStandardDeviation(self, asset_returns):
        standard_deviation = asset_returns.std()
        return standard_deviation

    def getSharpeRatio(self, average_return, standard_deviation):
        risk_free_rate = self.risk_free_rate
        sharpe_ratio = (average_return - risk_free_rate) / standard_deviation
        return sharpe_ratio

    def getDownsideReturns(self, asset_returns):
        downside_returns = asset_returns[asset_returns < 0]
        downside_deviation = downside_returns.std()
        return downside_returns

    def getSortinoRatio(self, asset_returns, average_return, downside_returns, risk_free_rate):
        downside_returns = asset_returns[asset_returns < 0]
        average_downside_return = downside_returns.mean()
        sortino_ratio = (average_return - risk_free_rate) / downside_returns.std()
        return sortino_ratio

    def getBenchmarkReturns(self, benchmark_data):
        benchmark_returns = benchmark_data["Close"].pct_change().dropna()
        return benchmark_returns

    def getBeta(self, asset_returns, benchmark_returns):
        model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
        beta = model.params[1]
        return beta

    def getAlpha(self, asset_returns, benchmark_returns, beta):
        model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
        alpha = model.params[0]
        return alpha

    def getTreynorRatio(self, average_return, risk_free_rate, beta):
        treynor_ratio = (average_return - risk_free_rate) / beta
        return treynor_ratio
    
    def getInformationRatio(self, asset_returns, benchmark_returns):
        tracking_error = np.sqrt(np.mean((asset_returns - benchmark_returns) ** 2))
        information_ratio = (asset_returns - benchmark_returns).mean() / tracking_error
        return information_ratio

    def getMaxDrawdown(self, asset_returns):
        cumulative_returns = (asset_returns + 1).cumprod()
        cumulative_max = cumulative_returns.cummax()
        drawdown = (cumulative_max - cumulative_returns) / cumulative_max
        return drawdown

    def getVaR(self, asset_returns):
        confidence_level = 0.95
        var = np.percentile(asset_returns, 100-confidence_level * 100)
        return var

    def getCVaR(self, asset_returns):
        var = self.getVaR(asset_returns)
        confidence_level = 0.95
        cvar = asset_returns[asset_returns <= var].mean()
        return cvar

    def getRSquared(self, asset_returns, benchmark_returns):
        model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
        r_squared = model.rsquared
        return r_squared   
    
    def getCorrelation(self, asset_returns, benchmark_returns):
        correlation = asset_returns.corr(benchmark_returns)
        return correlation

    def getVolatility(self, asset_returns):
        volatility = asset_returns.std()
        return volatility

    def getSkewness(self, asset_returns):
        skewness = asset_returns.skew()
        return skewness

    def getKurtosis(self, asset_returns):
        kurtosis = asset_returns.kurtosis()
        return kurtosis

    def getJarqueBera(self, asset_returns):
        jarque_bera = sm.stats.stattools.jarque_bera(asset_returns)
        return jarque_bera

    def plotGraph(self, drawdown, ticker):
        plt.plot(drawdown)
        plt.title("Max Drawdown of {}".format(ticker))
        plt.xlabel("Date")
        plt.ylabel("Drawdown")
        try:
            plt.show()
        except:
            pass
        max_drawdown = drawdown.max()

    

def printInfo(sym,avg_ret,stdev,shrp,srt,beta,alpha,treynor,info,var,cvar,r_squared,correlation,volatility,skewness,kurtosis,jarque_bera):
    print("\nRisk Management Analytics: {}".format(sym))
    
    print("Average Return: {}\n".format(avg_ret))
    print("Standard Deviation: {}".format(stdev))
    print("Sharpe Ratio: {}".format(shrp))
    print("Sortino Ratio: {}".format(srt))
    print("Beta: {}".format(beta))
    print("Alpha: {}".format(alpha))
    print("Treynor Ratio: {}".format(treynor))
    print("Information Ratio: {}".format(info))
 
    print("Value at Risk: {}".format(var))
    print("Conditional Value at Risk: {}".format(cvar))
    print("R Squared: {}".format(r_squared))
    print("Correlation: {}".format(correlation))
    print("Volatility: {}".format(volatility))
    print("Skewness: {}".format(skewness))
    print("Kurtosis: {}".format(kurtosis))
    print("Jarque Bera: {}".format(jarque_bera))

def main():

    # define the requirements 
    ticker = 'AAPL'
    benchmark_ticker = '^GSPC'
    start_date = '2010-01-01'
    end_date = '2020-12-31'
    risk_free_rate = 0.03

    # create an instance of the RiskAnalysis class
    risk_analysis   = RiskAnalysis(ticker, benchmark_ticker, start_date, end_date, risk_free_rate)
    # create historical and benchmark dataset
    hs              = risk_analysis.getHistoricalData(ticker, start_date, end_date)
    bd              = risk_analysis.getBenchmarkData(benchmark_ticker, start_date, end_date)
    # get returns
    arets, brets    = risk_analysis.getReturns(hs, bd)

    # get the required values
    avg_ret         = risk_analysis.getAverageReturn(arets)
    stdev           = risk_analysis.getStandardDeviation(arets)
    shrp            = risk_analysis.getSharpeRatio(avg_ret, stdev)
    drets           = risk_analysis.getDownsideReturns(arets)
    sortino         = risk_analysis.getSortinoRatio(arets, avg_ret, drets, risk_free_rate)
    beta            = risk_analysis.getBeta(arets, brets)
    alpha           = risk_analysis.getAlpha(arets, brets, beta)
    tr              = risk_analysis.getTreynorRatio(avg_ret, risk_free_rate, beta)
    ir              = risk_analysis.getInformationRatio(arets, brets)
    maxd            = risk_analysis.getMaxDrawdown(arets)
    var             = risk_analysis.getVaR(arets)
    cvar            = risk_analysis.getCVaR(arets)
    rs              = risk_analysis.getRSquared(arets, brets)
    corr            = risk_analysis.getCorrelation(arets, brets)
    vol             = risk_analysis.getVolatility(arets)
    skew            = risk_analysis.getSkewness(arets)
    k               = risk_analysis.getKurtosis(arets)
    jb              = risk_analysis.getJarqueBera(arets)

    # plot the graph
    crets = (arets + 1).cumprod()
    cmax = crets.cummax()
    drawdown = (cmax - crets) / cmax

    printInfo(avg_ret,stdev,shrp,sortino,beta,alpha,tr,ir,var,cvar,rs,corr,vol,skew,k,jb)
    risk_analysis.plotGraph(drawdown, ticker)
    

if __name__ == "__main__":
    # main()
    pass

    # define the requirements
    # ticker = 'AAPL'
    # benchmark_ticker = '^GSPC'
    # start_date = '2010-01-01'
    # end_date = '2020-12-31'

    # fetch historical price data for the asset and the benchmark
    # asset_data = yf.download(ticker, start_date, end_date)
    # benchmark_data = yf.download(benchmark_ticker, start_date, end_date)

    # Extract the "close" prices from the data
    # asset_prices = asset_data["Close"]
    # benchmark_prices = benchmark_data["Close"]

    # Calculate the asset returns and benchmark returns
    # asset_returns = asset_prices.pct_change().dropna()
    # benchmark_returns = benchmark_prices.pct_change().dropna()

    # Calculate the average return
    # average_return = asset_returns.mean()

    # Standard Deviation
    # standard_deviation = asset_returns.std()
    # print("Standard Deviation: ",standard_deviation)

    # Sharpe Ratio
    # risk_free_rate = 0.03 # Assume a risk-free rate of 3%
    # sharpe_ratio = (average_return - risk_free_rate) / standard_deviation
    # print("Sharpe Ratio: ",sharpe_ratio)

    # Sortino Ratio
    # downside_returns = asset_returns[asset_returns < 0]
    # average_downside_return = downside_returns.mean()
    # print("Average Downside Return: ",average_downside_return)
    # sortino_ratio = (average_return - risk_free_rate) / downside_returns.std()
    # print("Sortino Ratio: ",sortino_ratio)

    # Beta
    # model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
    # beta = model.params[1]

    # Max Drawdown
    # cumulative_returns = (asset_returns + 1).cumprod()
    # print("Cumulative Returns: ",cumulative_returns)
    # cumulative_max = cumulative_returns.cummax()
    # print("Cumulative Max: ",cumulative_max)
    # drawdown = (cumulative_max - cumulative_returns) / cumulative_max
    # print("Drawdown: ",drawdown)

    # Value at Risk (VaR)
    # confidence_level = 0.95
    # var = np.percentile(asset_returns, 100-confidence_level * 100)
    # print("Confidence Level: ",confidence_level)
    # print("VaR: ",var)

    # Conditional Value at Risk (CVaR)
    # tail_returns = asset_returns[asset_returns < var]
    # cvar = tail_returns.mean()
    # print("CVaR: ",cvar)

    # R-squared
    # model = sm.OLS(asset_returns, sm.add_constant(benchmark_returns)).fit()
    # r_squarded = model.rsquared
    # print("R-Squared: ",r_squarded)

    # Plot 
    # plt.plot(drawdown)
    # plt.title("Max Drawdown of {}".format(ticker))
    # plt.xlabel("Date")
    # plt.ylabel("Drawdown")
    # plt.show()
    # max_drawdown = drawdown.max()
