"""

    This will display and gather current Macro Economic data. Macroeconomics is a branch
    of economics that deals with the performance, structure, behavioor, and decision-making
    of an economy as a whole. This includes intrest rates, taxes, and sovernment spending
    to regulate an economy's groth and stability. This includes regional, national, and
    global economies.

    Thins to take into consideration: GDP (Gross Domestic Product), uneployment rates,
    national income, price indices, output, consumption, inflation, saving, investment, 
    energy, interational trade, and international finance.

    - https://en.wikipedia.org/wiki/Macroeconomics

    

"""

import streamlit as st
import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import datetime

# import config as cf


# # Crude Oil Data frame
# oil = pd.DataFrame(quandl.get("FRED/DCOILWTICO", start_date=start_date, end_date=end_date, collapse="daily"))
# print(oil)


# unemployment = pd.DataFrame(quandl.get("FRED/UNRATE", start_date="2000-12-31", end_date="2020-04-20"))
# print(unemployment)

class MacroEco:
    def __init__(self, start_time, end_time):
        self.api_key = 'HMsNFYjwQumm3zSQPn9D'
        self.start_time = start_time
        self.end_time = end_time

        quandl.ApiConfig.api_key = self.api_key
        
    def getGDP(self):


        pass

    def getCrudeOilTrends(self):
        try:
            oil_df = pd.DataFrame(quandl.get("FRED/DCOILWTICO", start_date=self.start_time, end_date=self.end_time, collapse="daily"))
        except Exception as e:
            print(e)
        return oil_df

    def getUnemploymentTrends(self):
        try:
            unemployment_df = pd.DataFrame(quandl.get("FRED/UNRATE", start_date=self.start_time, end_date=self.end_time))
        except Exception as e:
            print(e)
        return unemployment_df


m = MacroEco("2000-12-31", "2020-04-20")

oil_df = m.getCrudeOilTrends()
 
# plt.plot(oil_df)


class FREDAPI:
    def __init__(self, api_key):
        self.api_key = api_key  