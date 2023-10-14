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
        
        # Streamlit App
        st.title('Financial Analysis')
        st.write('This app displays the fundamental financial data.')
        
        # Creating tabs for different DataFrames
        tab = st.selectbox("Choose a Financial Statement", ["Balance Sheet", "Income Statement"])
        if tab == "Balance Sheet":
            st.write(df_bs)
        elif tab == "Income Statement":
            st.write(df_is)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

