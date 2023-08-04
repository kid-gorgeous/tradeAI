""" 
    This is a streamlit app that will allow you to visualize technical indicators 
    for any stock. It's currently a work in progress. The restful api is not yet
    working. I'm not sure if I'll be able to get it to work. 

    TODO: to fix this module, the symbol pages from the symbols directory will be used
    to populate the dropdown menu, graphs, charts, etc.
 """

import yfinance as yf
import streamlit as st
import datetime 
import pandas as pd
import pandas_ta as ta
import requests
yf.pdr_override()

class App:
    def __init__(self):
        self.symbol, self.start, self.end = user_input_features()
        self.company_name = self.symbol.upper()
        self.titleText, self.introText = ""
        self.data = None

        self.header = 'User Input Parameters'
        self.today = datetime.date.today()

    def getData(self):
        self.data = yf.download(self.symbol,self.start,self.end)

    def run(self):
        pass


st.title('TA App')
st.write("""
## Technical Analysis Web Application
Shown below are the **Moving Average Crossovers**, **Bollinger Bands**, **MACD's**, **Commodity Channel Indexes**, and **Relative Strength Indexes** of any stock!
""")

st.sidebar.header('User Input Parameters')

# Sidebar
today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start_date, end_date = user_input_features()
company_name = symbol.upper() # get_symbol(symbol.upper())
start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

# Read data 
data = yf.download(symbol,start,end)
data['SMA'] = ta.sma(data['Adj Close'], timeperiod = 20)
data['EMA'] = ta.ema(data['Adj Close'], timeperiod = 20)

# Plot
st.header(f"SMA vs. EMA for the Adjusted Closing price: \n {company_name}")
st.line_chart(data[['Adj Close','SMA','EMA']])

import sys
sys.path.append('scripts')
from risk_mgmt import RiskAnalysis, printInfo
from sentiment_analysis import SA, News

benchmark_symbol = '^GSPC'
risk_analysis = RiskAnalysis(symbol, benchmark_symbol,start,end, 0.03)

hs = risk_analysis.getHistoricalData(symbol,start,end)
bd = risk_analysis.getBenchmarkData(benchmark_symbol,start,end)
arets, brets = risk_analysis.getReturns(hs,bd)

with st.expander("Risk Analysis"):
    # get the required values
    avg_ret         = risk_analysis.getAverageReturn(arets)
    stdev           = risk_analysis.getStandardDeviation(arets)
    shrp            = risk_analysis.getSharpeRatio(avg_ret, stdev)
    drets           = risk_analysis.getDownsideReturns(arets)
    sortino         = risk_analysis.getSortinoRatio(arets, avg_ret, drets, risk_free_rate=0.03)
    beta            = risk_analysis.getBeta(arets, brets)
    alpha           = risk_analysis.getAlpha(arets, brets, beta)
    tr              = risk_analysis.getTreynorRatio(avg_ret, 0.03, beta)
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

    st.write(f"""
    #### Data for the stock {company_name} 
    from {start_date} to {end_date}


    | Metric | Value |
    | ------ | ----- |
    | Average Return | {avg_ret} |
    | Standard Deviation | {stdev} |
    | Sharpe Ratio | {shrp} |
    | Sortino Ratio | {sortino} |
    | Beta | {beta} |
    | Alpha | {alpha} |
    | Treynor Ratio | {tr} |
    | Information Ratio | {ir} |
    | Value at Risk | {var} |
    | Conditional Value at Risk | {cvar} |
    | R-Squared | {rs} |
    | Correlation | {corr} |
    | Volatility | {vol} |
    | Skewness | {skew} |
    | Kurtosis | {k} |
    | Jarque-Bera | {jb} |
    
    """)
try: 
    news = News(symbol,tickers=[symbol])
    news = news.getNews()
    st.header(f"News for {company_name}")
    st.table(news)
except:
    pass
    
try:
    sa = SA(symbol,tickers=[symbol])
    s_index, mean_index = sa.sentimentAnalysis()
    st.header(f"Sentiment Analysis for {company_name}")
    st.table(s_index)
    st.table(mean_index)
except:
    pass

    # # Bollinger Bands
    # data['lower_band'], data['middle_band'], data['upper_band'] = ta.bbands(data['Adj Close'], length =20)

    # # Plot
    # st.header(f"Bollinger Bands\n {company_name}")
    # st.line_chart(data[['Adj Close','upper_band','middle_band','lower_band']])

    # ## MACD (Moving Average Convergence Divergence)
    # MACD
    # data['macd'], data['macdsignal'], data['macdhist'] = ta.macd(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    # data['macd'], data['macdsignal'], data['macdhist'] = talib.MACD(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    # # Plot
    # st.header(f"Moving Average Convergence Divergence\n {company_name}")
    # st.line_chart(data[['macd','macdsignal']])

    # ## CCI (Commodity Channel Index)
    # # CCI
    # cci = ta.trend.cci(data['High'], data['Low'], data['Close'], n=31, c=0.015)

    # # Plot
    # st.header(f"Commodity Channel Index\n {company_name}")
    # st.line_chart(cci)

    # ## RSI (Relative Strength Index)
    # RSI
    # data['RSI'] = ta.rsi(data['Adj Close'], timeperiod=14)

    # # Plot
    # st.header(f"Relative Strength Index\n {company_name}")
    # st.line_chart(data['RSI'])

    # # ## OBV (On Balance Volume)
    # # OBV
    # data['OBV'] = ta.obv(data['Adj Close'], data['Volume'])/10**6

    # # Plot
    # st.header(f"On Balance Volume\n {company_name}")
    # st.line_chart(data['OBV'])
