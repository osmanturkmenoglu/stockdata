import numpy as np
import pandas as pd
import requests
import datetime
import calendar
import scipy.stats as stats
import matplotlib.pyplot as plt
import streamlit as st
from st_aggrid import AgGrid


import os
from eod import EodHistoricalData




# Accessing API key from secrets.toml
api = st.secrets["my_secrets"]["api_key"]


# Create the client instance
client = EodHistoricalData(api)

def page1():
    st.title('Financial Analysis')
    st.write('This app displays the fundamental financial data.')

    # Set default values for inputs
    default_symbol = "AAPL.US"
    default_frequency = "yearly"

    # Inputs for symbol and frequency
    symbol = st.text_input("Please enter the stock symbol and exchange code (e.g., AAPL.US):", default_symbol)
    frequency = st.selectbox("Choose data frequency:", ["yearly", "quarterly"], index=0 if default_frequency == "yearly" else 1)

    # Button to fetch data
    if st.button("Get Data") and symbol.strip():
        try:
            # Fetching Balance Sheet data
            resp_bs = client.get_fundamental_equity(symbol, filter_=f'Financials::Balance_Sheet::{frequency}')
            df_bs = pd.DataFrame.from_dict(resp_bs, orient='index')
            df_bs = df_bs.drop(columns=['date'])
            df_bs.index.name = 'date'
            
            # Specify columns to convert for Balance Sheet
            cols_to_convert_bs = ['totalAssets', 'totalLiab', 'totalStockholderEquity', 'totalCurrentLiabilities', 'intangibleAssets', 'totalCurrentAssets', 'netInvestedCapital', 'otherCurrentAssets', 'otherCurrentLiab', 'deferredLongTermLiab', 'commonStock', 'capitalStock', 'retainedEarnings', 'otherLiab', 'goodWill', 'otherAssets', 'cash', 'cashAndEquivalents', 'currentDeferredRevenue', 'netDebt', 'shortTermDebt', 'shortLongTermDebt', 'shortLongTermDebtTotal', 'otherStockholderEquity', 'propertyPlantEquipment', 'longTermInvestments', 'netTangibleAssets', 'shortTermInvestments', 'netReceivables', 'longTermDebt', 'inventory', 'accountsPayable', 'accumulatedOtherComprehensiveIncome', 'commonStockTotalEquity', 'retainedEarningsTotalEquity', 'nonCurrrentAssetsOther', 'nonCurrentAssetsTotal', 'capitalLeaseObligations', 'longTermDebtTotal', 'nonCurrentLiabilitiesOther', 'nonCurrentLiabilitiesTotal', 'capitalSurpluse', 'liabilitiesAndStockholdersEquity', 'cashAndShortTermInvestments', 'propertyPlantAndEquipmentGross', 'propertyPlantAndEquipmentNet', 'netWorkingCapital', 'commonStockSharesOutstanding']
            df_bs[cols_to_convert_bs] = df_bs[cols_to_convert_bs].applymap(lambda x: f'{float(x)/1e9:.2f}B' if pd.notnull(x) else x)
            
            # Fetching Income Statement data
            resp_is = client.get_fundamental_equity(symbol, filter_=f'Financials::Income_Statement::{frequency}')
            df_is = pd.DataFrame.from_dict(resp_is, orient='index')
            df_is = df_is.drop(columns=['date'])
            df_is.index.name = 'date'
            
            # Specify columns to convert for Income Statement
            cols_to_convert_is = ['researchDevelopment', 'effectOfAccountingCharges', 'incomeBeforeTax', 'minorityInterest', 'netIncome', 'sellingGeneralAdministrative', 'grossProfit', 'reconciledDepreciation', 'ebit', 'ebitda', 'depreciationAndAmortization', 'nonOperatingIncomeNetOther', 'operatingIncome', 'otherOperatingExpenses', 'interestExpense', 'taxProvision', 'interestIncome', 'netInterestIncome', 'extraordinaryItems', 'nonRecurring', 'otherItems', 'incomeTaxExpense', 'totalRevenue', 'totalOperatingExpenses', 'costOfRevenue', 'totalOtherIncomeExpenseNet', 'discontinuedOperations', 'netIncomeFromContinuingOps', 'netIncomeApplicableToCommonShares', 'preferredStockAndOtherAdjustments']
            df_is[cols_to_convert_is] = df_is[cols_to_convert_is].applymap(lambda x: f'{float(x)/1e9:.2f}B' if pd.notnull(x) else x)
            
            # Displaying DataFrames side by side
            col1, col2 = st.columns(2)
            with col1:
                st.header("Balance Sheet")
                st.dataframe(df_bs)
            with col2:
                st.header("Income Statement")
                st.dataframe(df_is)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Define other pages as functions
def page2():
    st.title('Page 2')
    st.write('This is the content of page 2.')
    # Add more Streamlit widgets for page 2 content

def page3():
    st.title('Page 3')
    st.write('This is the content of page 3.')
    # Add more Streamlit widgets for page 3 content

# Dictionary of pages
pages = {
    'Financial Analysis': page1,
    'Page 2': page2,
    'Page 3': page3,
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Render the selected page
if selection in pages:
    pages[selection]()
