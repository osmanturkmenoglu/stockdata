import numpy as np
import pandas as pd
import requests
import datetime
import calendar
import scipy.stats as stats
import matplotlib.pyplot as plt


import os
from eod import EodHistoricalData



api_key = '63caea0aebcd11.80376136'

# Create the client instance
client = EodHistoricalData(api_key)



symbol = input("Please enter the stock symbol and exchange code (e.g., AAPL.US): ")




resp = client.get_fundamental_equity(symbol, filter_='Financials::Balance_Sheet::yearly')

# Convert the dictionary to a Pandas DataFrame
df = pd.DataFrame.from_dict(resp, orient='index')

# Drop the 'date' column as it's the same as the index
df = df.drop(columns=['date'])

# Rename the index to 'date'
df.index.name = 'date'

# Create a copy of the DataFrame for plotting
df_plot = df.copy()

# Convert columns with large numbers to a readable format (in billions) for display
cols_to_convert = ['totalAssets', 'totalLiab', 'totalStockholderEquity', 'totalCurrentLiabilities', 'intangibleAssets', 'totalCurrentAssets', 'netInvestedCapital', 'otherCurrentAssets', 'otherCurrentLiab', 'deferredLongTermLiab', 'commonStock', 'capitalStock', 'retainedEarnings', 'otherLiab', 'goodWill', 'otherAssets', 'cash', 'cashAndEquivalents', 'currentDeferredRevenue', 'netDebt', 'shortTermDebt', 'shortLongTermDebt', 'shortLongTermDebtTotal', 'otherStockholderEquity', 'propertyPlantEquipment', 'longTermInvestments', 'netTangibleAssets', 'shortTermInvestments', 'netReceivables', 'longTermDebt', 'inventory', 'accountsPayable', 'accumulatedOtherComprehensiveIncome', 'commonStockTotalEquity', 'retainedEarningsTotalEquity', 'nonCurrrentAssetsOther', 'nonCurrentAssetsTotal', 'capitalLeaseObligations', 'longTermDebtTotal', 'nonCurrentLiabilitiesOther', 'nonCurrentLiabilitiesTotal', 'capitalSurpluse', 'liabilitiesAndStockholdersEquity', 'cashAndShortTermInvestments', 'propertyPlantAndEquipmentGross', 'propertyPlantAndEquipmentNet', 'netWorkingCapital', 'commonStockSharesOutstanding']
df[cols_to_convert] = df[cols_to_convert].applymap(lambda x: f'{float(x)/1e9:.2f}B' if pd.notnull(x) else x)



# Streamlit App
st.title('Apple Inc. Financial Analysis')
st.write('This app displays the fundamental financial data of Apple Inc.')
st.dataframe(df.head())
st.line_chart(df_plot[['totalAssets', 'totalLiab', 'totalStockholderEquity']].astype(float))

df


# Streamlit App
st.title('Apple Inc. Financial Analysis')
st.write('This app displays the fundamental financial data of Apple Inc.')
st.dataframe(df.head())
st.line_chart(df_plot[['totalAssets', 'totalLiab', 'totalStockholderEquity']].astype(float))
