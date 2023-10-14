import numpy as np
import pandas as pd
import requests
import datetime
import calendar
import scipy.stats as stats
import matplotlib.pyplot as plt


import os
from eod import EodHistoricalData


import streamlit as st

# Accessing API key from secrets.toml
api = st.secrets["my_secrets"]["api_key"]


# Create the client instance
client = EodHistoricalData(api)

default_symbol = "AAPL.US"
default_frequency = "yearly"

symbol = st.text_input("Please enter the stock symbol and exchange code (e.g., AAPL.US): ")
frequency = st.selectbox("Choose data frequency:", ["yearly", "quarterly"])


if st.button("Get Data") and symbol:
    try:
        # Fetching the data based on user input and selected frequency
        resp = client.get_fundamental_equity(symbol, filter_=f'Financials::Balance_Sheet::{frequency}')
        
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

        resp = client.get_fundamental_equity(symbol, filter_=f'Financials::Income_Statement::{frequency}')

        # Convert the dictionary to a Pandas DataFrame
        df = pd.DataFrame.from_dict(resp, orient='index')

        # Drop the 'date' column as it's the same as the index
        df = df.drop(columns=['date'])

        # Rename the index to 'date'
        df.index.name = 'date'

        # Create a copy of the DataFrame for plotting
        df_plot = df.copy()

        # Convert columns with large numbers to a readable format (in billions) for display
        # Identify columns that contain numerical values
        cols_to_convert = [
            'researchDevelopment', 'effectOfAccountingCharges', 'incomeBeforeTax', 'minorityInterest',
            'netIncome', 'sellingGeneralAdministrative', 'grossProfit', 'reconciledDepreciation', 'ebit', 'ebitda',
            'depreciationAndAmortization', 'nonOperatingIncomeNetOther', 'operatingIncome',
            'otherOperatingExpenses', 'interestExpense', 'taxProvision', 'interestIncome',
            'netInterestIncome', 'extraordinaryItems', 'nonRecurring', 'otherItems',
            'incomeTaxExpense', 'totalRevenue', 'totalOperatingExpenses', 'costOfRevenue',
            'totalOtherIncomeExpenseNet', 'discontinuedOperations', 'netIncomeFromContinuingOps',
            'netIncomeApplicableToCommonShares', 'preferredStockAndOtherAdjustments'
        ]
        df[cols_to_convert] = df[cols_to_convert].applymap(lambda x: f'{float(x)/1e9:.2f}B' if pd.notnull(x) else x)
        
        # Streamlit App
        st.title('Financial Analysis')
        st.write('This app displays the fundamental financial data.')
        st.write(df)
        st.line_chart(df_plot[['totalAssets', 'totalLiab', 'totalStockholderEquity']].astype(float))
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
