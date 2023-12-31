"""
    Using peices of code from https://towardsdatascience.com/stock-news-sentiment-analysis-with-python-193d4b4378d4
    an algorithm is created and adjusted to fit marked parameters.

    This will quickly parse and calculate to sentiment of the news headlines for any inputted ticker 
    by using FinViz to give access to an incredible amount of information including interactive
    charts, over 70 fundemntal ratios, large bank trading data, and updated news headlines
    for any ticker symbol. 


"""
import time

# Import libraries
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import nltk
nltk.download('vader_lexicon')
print('\n')

class News:
    def __init__(self, symbol, tickers):
        self.n = 3
        self.symbol = symbol
        self.tickers = tickers

    def getNews(self):
        n = self.n
        
        finwiz_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}

        for ticker in self.tickers:
            url = finwiz_url + ticker
            req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0'}) 
            resp = urlopen(req)    
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id='news-table')
            news_tables[ticker] = news_table

        # using news_tables to get the news headlines
        news_dataframe = pd.DataFrame(columns=['Ticker', 'Headline', 'Date', 'URL'])
        try:
            for ticker in self.tickers:
                df = news_tables[ticker]
                df_tr = df.findAll('tr')

                for i, table_row in enumerate(df_tr):
                    a_text = table_row.a.text
                    td_text = table_row.td.text
                    td_text = td_text.strip()
                    url_text = table_row.a.get('href')
                    
                    new_row = {'Ticker': ticker, 'Headline': a_text, 'Date': td_text, 'URL': url_text}
                    news_dataframe = pd.concat([news_dataframe, pd.DataFrame([new_row])], ignore_index=True)

                    if i == n-1:
                        break
                           

        except KeyError:
            pass

        return news_dataframe

class SA:
    def __init__(self, symbol, tickers):
        self.n = 3
        self.symbol = symbol
        self.tickers = tickers

        
    def getNewsTables(self):
        finwiz_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}

        for ticker in self.tickers:
            url = finwiz_url + ticker
            req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0'}) 
            resp = urlopen(req)    
            html = BeautifulSoup(resp, features="lxml")
            news_table = html.find(id='news-table')
            news_tables[ticker] = news_table

        return news_tables

    def getData(self):
        n = self.n
        news_tables = self.getNewsTables()

        # using news_tables to get the news headlines
        news_dataframe = pd.DataFrame(columns=['Ticker', 'Headline', 'Date', 'URL'])
        try:
            for ticker in self.tickers:
                df = news_tables[ticker]
                df_tr = df.findAll('tr')

                for i, table_row in enumerate(df_tr):
                    a_text = table_row.a.text
                    td_text = table_row.td.text
                    td_text = td_text.strip()
                    url_text = table_row.a.get('href')
                    
                    # create an append method that adds the headline and the url to a list
                    news_dataframe = news_dataframe.concat({'Ticker': ticker, 'Headline': a_text, 'Date': td_text, 'URL': url_text}, ignore_index=True)
                    
                    if i == n-1:
                        break
                           

        except KeyError:
            pass

        return news_dataframe

    def parseData(self):
        news_tables = self.getNewsTables()
        try:
            parsed_news = []
            count = 0
            for file_name, news_table in news_tables.items():
                # for all the table rows in a news table
                for x in news_table.findAll('tr'):
                    try:
                        text = x.a.text
                        date_scrape = x.td.text.split()
                    except:
                        pass

                    if len(date_scrape) == 1:
                        time = date_scrape[0]
                        
                    else:
                        date = date_scrape[0]
                        time = date_scrape[1]

                    ticker = file_name.split('_')[0]
                    parsed_news.append([ticker, date, time, text])
        except:
            pass

        return parsed_news

    def sentimentAnalysis(self):
        symbol = self.symbol

        parsed_news = self.parseData()
        analyzer = SentimentIntensityAnalyzer()
        columns = ['Ticker', 'Date', 'Time', 'Headline']
        news = pd.DataFrame(parsed_news, columns=columns)
        scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

        df_scores = pd.DataFrame(scores)
        news = news.join(df_scores, rsuffix='_right')

        news['Date'] = pd.to_datetime(news.Date).dt.date
        unique_ticker = news['Ticker'].unique().tolist()
        news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

        values = []
        dataframe = None
        for ticker in self.tickers: 
            dataframe = news_dict[ticker]
            dataframe = dataframe.set_index('Ticker')
            dataframe = dataframe.drop(columns = ['Headline'])
            mean = round(dataframe['compound'].mean(), 2)
            values.append(mean)

        df = pd.DataFrame(list(zip(self.tickers, values)), columns =['Ticker', 'Mean Sentiment']) 
        df = df.set_index('Ticker')
        df = df.sort_values('Mean Sentiment', ascending=False)

        return dataframe.head(), df

def main():
    sa = SA('AAPL',tickers=['AAPL'])
    sa.sentimentAnalysis()
    
if __name__ == "__main__":
    # main()

    # Get Data
    # finwiz_url = 'https://finviz.com/quote.ashx?t='
    # news_tables = {}

    # for ticker in tickers:
    #     url = finwiz_url + ticker
    #     req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0'}) 
    #     resp = urlopen(req)    
    #     html = BeautifulSoup(resp, features="lxml")
    #     news_table = html.find(id='news-table')
    #     news_tables[ticker] = news_table

    # try:
    #     for ticker in tickers:
    #         df = news_tables[ticker]
    #         df_tr = df.findAll('tr')
        
    #         print ('\n')
    #         print ('Recent News Headlines for {}: '.format(ticker))
            
    #         for i, table_row in enumerate(df_tr):
    #             a_text = table_row.a.text
    #             td_text = table_row.td.text
    #             td_text = td_text.strip()
    #             print(a_text,'(',td_text,')')
    #             if i == n-1:
    #                 break
    # except KeyError:
    #     pass

    # Iterate through the news
    # parsed_news = []
    # count = 0
    # for file_name, news_table in news_tables.items():
    #     # for all the table rows in a news table
    #     for x in news_table.findAll('tr'):
    #         try:
    #             text = x.a.text
    #             date_scrape = x.td.text.split()
    #         except:
    #             pass

    #         if len(date_scrape) == 1:
    #             time = date_scrape[0]
                
    #         else:
    #             date = date_scrape[0]
    #             time = date_scrape[1]

    #         ticker = file_name.split('_')[0]
    #         parsed_news.append([ticker, date, time, text])

    # inb = input("\nPress Enter to continue...(Sentiment Analysis)")  
    # sa = SA(3, ['AAPL', 'TSLA', 'AMZN'])
    # parsed_news = sa.parseData()
            
    # # Sentiment Analysis
    # analyzer = SentimentIntensityAnalyzer()
    # columns = ['Ticker', 'Date', 'Time', 'Headline']
    # news = pd.DataFrame(parsed_news, columns=columns)
    # scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    # df_scores = pd.DataFrame(scores)
    # news = news.join(df_scores, rsuffix='_right')

    # View Data 
    # news['Date'] = pd.to_datetime(news.Date).dt.date

    # unique_ticker = news['Ticker'].unique().tolist()
    # news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    # values = []
    # for ticker in sa.tickers: 
    #     dataframe = news_dict[ticker]
    #     dataframe = dataframe.set_index('Ticker')
    #     dataframe = dataframe.drop(columns = ['Headline'])
    #     print ('\n')
    #     print (dataframe.head())
        
    #     inb = input("\nPress Enter to continue... (List of Sentiment Values)") 
    #     mean = round(dataframe['compound'].mean(), 2)
    #     values.append(mean)
        
    # df = pd.DataFrame(list(zip(sa.tickers, values)), columns =['Ticker', 'Mean Sentiment']) 
    # df = df.set_index('Ticker')
    # df = df.sort_values('Mean Sentiment', ascending=False)
    # print ('\n')
    # print (df)
    pass
