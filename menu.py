""" 
    This menu is a work in progress; for right now it will only display information
    from the symbol CSV files. It will display the following information: Date, Open,
    High, Low, Close, Adj Close, Volume.

    The menu will allow the user to search from a directory of symbols downloaded from 
    the S&P 500. The user will be able to search for a symbol and the menu will display
    the information from the CSV file for that symbol. It will also display the sentiment
    analysis for that symbol. 

"""

import csv
import pandas
import termcolor

from risk_mgmt import RiskAnalysis, printInfo
from sentiment_analysis import SA, News

# Working
def openfile(inp):
    filename = inp
    with open(f'symbols/{filename}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            print(', '.join(row))

class Menu:
    # Simply name the file to search
    def __init__(self, filename):
        self.filename = filename
        self.symbol = filename

    def getSymbols(self):
        self.symbol = filename
        
    def getScreen(self):
        pass
    
    def getSentimentAnalysis(self):
        symbol = self.symbol
        try:
            sa = SA(symbol,tickers=[symbol])
            sa.sentimentAnalysis()
        except:
            print('Error: No sentiment analysis for this symbol.\n')

    def getNews(self):
        symbol = self.symbol
        try:
            news = News(symbol,tickers=[symbol])
            news.getNews()
        except:
            print('Error: No news for this symbol.\n')

    def getRiskAnalysis(self):
        # define the requirements 
        symbol = self.symbol
        benchmark_ticker = '^GSPC'
        start_date = '2010-01-01'
        end_date = '2020-12-31'
        risk_free_rate = 0.03

        # create an instance of the RiskAnalysis class
        risk_analysis   = RiskAnalysis(symbol, benchmark_ticker, start_date, end_date, risk_free_rate)
        # create historical and benchmark dataset
        hs              = risk_analysis.getHistoricalData(symbol, start_date, end_date)
        bd              = risk_analysis.getBenchmarkData(benchmark_ticker, start_date, end_date)
        # get returns
        arets, brets      = risk_analysis.getReturns(hs, bd)
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
        printInfo(symbol,avg_ret,stdev,shrp,sortino,beta,alpha,tr,ir,var,cvar,rs,corr,vol,skew,k,jb)
        risk_analysis.plotGraph(drawdown, symbol)
        pass

# Only spits out a cvs dataframe BUT the query works
while True:
    inp = input("\nEnter a symbol: ")
    menu = Menu(inp.upper())    

    menu.getSentimentAnalysis()
    menu.getNews()
    menu.getRiskAnalysis()