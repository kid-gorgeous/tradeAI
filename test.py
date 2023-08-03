import pandas_ta as ta
import pandas as pd
import yfinance as yf
import datetime


today = datetime.date.today()
start_date = "2019-01-01"
# Sidebar
today = datetime.date.today()
def user_input_features():
    ticker = "AAPL"
    start_date = "2019-01-01"
    end_date = today
    return ticker, start_date, end_date

symbol, start, end = user_input_features()
company_name = symbol.upper() # get_symbol(symbol.upper())
start = pd.to_datetime(start)
end = pd.to_datetime(end)
start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data 
data = yf.download(symbol,start,end)

# Bollinger Bands
df = ta.bbands(data['Adj Close'], length =20)
# data['BBL_20_2.0'], data['BBM_20_2.0'], data['BBU_20_2.0'] = ta.bbands(data['Adj Close'], length =20)
print(type(ta.bbands(data['Adj Close'], length =20, std=1.5)))