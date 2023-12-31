""" 
    This is a streamlit app that will allow you to visualize technical indicators 
    for any stock. It's currently a work in progress. The restful api is not yet
    working. I'm not sure if I'll be able to get it to work. 

    TODO: to fix this module, the symbol pages from the symbols directory will be used
    to populate the dropdown menu, graphs, charts, etc.

    TODO: at some point add a real exception handler to the code... lol
 """

import yfinance as yf
import macroeco
import streamlit as st
import datetime 
import pandas as pd
import pandas_ta as ta
import requests
yf.pdr_override()

import config as cf

st.title(cf.spa_name)
st.write(cf.intro)

st.sidebar.header(cf.header)

# Sidebar
today = datetime.date.today()
def user_input_features():
    try:
        ticker = st.sidebar.text_input("Ticker", 'AAPL')
        start_date = st.sidebar.text_input("Start Date", '2013-01-01')
        end_date = st.sidebar.text_input("End Date", f'{today}')
        return ticker, start_date, end_date
    except:
        pass

symbol, start_date, end_date = user_input_features()
company_name = symbol.upper()
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

try:
    benchmark_symbol = cf.benchmark_symbol
    risk_analysis = RiskAnalysis(symbol, benchmark_symbol,start,end, 0.03)

    hs = risk_analysis.getHistoricalData(symbol,start,end)
    bd = risk_analysis.getBenchmarkData(benchmark_symbol,start,end)
    arets, brets = risk_analysis.getReturns(hs,bd)


    # TODO: Write a better table function that will display and provide detail definitions 
    # for each metric upon request

    with st.expander("Risk Analysis"):
        # get the required values
        # The average return of the stock
        avg_ret         = risk_analysis.getAverageReturn(arets)
        # The standard deviation of the stock
        stdev           = risk_analysis.getStandardDeviation(arets)
        # The sharpe ratio of the stock is a measure of an investment's risk adjusted performance, calculated by comparing its return to that of a risk-free asset
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

        with st.container():
            st.text(f"Average Return: {avg_ret}.")
            st.text(f"Standard Deviation: {stdev}")
            st.text(f"Sharpe Ratio: {shrp}")
            st.text(f"Sortino Ratio: {sortino}")
            st.text(f"Beta: {beta}")
            st.text(f"Alpha: {alpha}")
            st.text(f"Treynor Ratio: {tr}")
            st.text(f"Information Ratio: {ir}")
            st.text(f"Value at Risk: {var}")
            st.text(f"Conditional Value at Risk: {cvar}")
            st.text(f"R-Squared: {rs}")
            st.text(f"Correlation: {corr}")
            st.text(f"Volatility: {vol}")
            st.text(f"Skewness: {skew}")
            st.text(f"Kurtosis: {k}")
            st.text(f"Jarque-Bera: {jb}")


        # st.write(f"""
        # #### Data for the stock {company_name} 
        #     from {start_date} to {end_date}
        #     # | Metric | Value |
        #     # | ------ | ----- |
        #     # | Average Return | {avg_ret} |
        #     # | Standard Deviation | {stdev} |
        #     # | Sharpe Ratio | {shrp} |
        #     # | Sortino Ratio | {sortino} |
        #     # | Beta | {beta} |
        #     # | Alpha | {alpha} |
        #     # | Treynor Ratio | {tr} |
        #     # | Information Ratio | {ir} |
        #     # | Value at Risk | {var} |
        #     # | Conditional Value at Risk | {cvar} |
        #     # | R-Squared | {rs} |
        #     # | Correlation | {corr} |
        #     # | Volatility | {vol} |
        #     # | Skewness | {skew} |
        #     # | Kurtosis | {k} |
        #     # | Jarque-Bera | {jb} |
        # """)
except:
    pass

try: 

    # TODO: Write a function that will allow for the user to click URLS, read specific 
    # sentiment artifacts include key words, phrases, and important symbols that can be 
    # identified with Machine Learning.
    news = News(symbol,tickers=[symbol])

    news = news.getNews()
    st.header(f"News for {company_name}")

    for i in range(len(news)):
        print(news[i]['URL'])
        

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


try:
    st.header("Macroeconomic Environment")

    me = macroeco.MacroEco(start_date, end_date)
    oil_df = me.getCrudeOilTrends()
    unemp_df = me.getUnemploymentTrends()

    st.write("### Crude Oil Trends")
    st.table(oil_df.tail(5))
    st.line_chart(oil_df['Value'])

    st.write("### Unemployment Trends")
    st.table(unemp_df.tail(5))

    st.line_chart(unemp_df['Value'])
except:
    pass
