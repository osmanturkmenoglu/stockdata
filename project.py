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
client = EodHistoricalData(API)

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
            
			try:
			    # Displaying DataFrames side by side
			    col1, col2 = st.columns(2)
			
			    # For the Balance Sheet DataFrame
			    with col1:
			        st.header("Balance Sheet")
			        # Multiselect widget to select columns for Balance Sheet
			        selected_columns_bs = st.multiselect('Select columns for Balance Sheet:', df_bs.columns, key='1')
			        # Filter the DataFrame based on selected columns
			        if selected_columns_bs:
			            filtered_df_bs = df_bs[selected_columns_bs]
			        else:
			            filtered_df_bs = df_bs  # If no columns are selected, display all
			        st.dataframe(filtered_df_bs)
			
			    # For the Income Statement DataFrame
			    with col2:
			        st.header("Income Statement")
			        # Multiselect widget to select columns for Income Statement
			        selected_columns_is = st.multiselect('Select columns for Income Statement:', df_is.columns, key='2')
			        # Filter the DataFrame based on selected columns
			        if selected_columns_is:
			            filtered_df_is = df_is[selected_columns_is]
			        else:
			            filtered_df_is = df_is  # If no columns are selected, display all
			        st.dataframe(filtered_df_is)
			
			except Exception as e:
			    st.error(f"An error occurred: {str(e)}")



# Define other pages as functions
def page2():
    st.title('Historical Multiples')
    st.write('This app displays the historical multiples data.')
    # Set default values for inputs
    default_symbol = "AAPL.US"
    default_frequency = "yearly"

    # Inputs for symbol and frequency
    symbol = st.text_input("Please enter the stock symbol and exchange code (e.g., AAPL.US):", default_symbol)
    frequency = st.selectbox("Choose data frequency:", ["yearly", "quarterly"], index=0 if default_frequency == "yearly" else 1)

    # Button to fetch data
    if st.button("Get Data") and symbol.strip():
        try:
            # Assuming resp1 and resp2 are the responses from your API calls and they are in a format that pandas can read (like a dict or a list of dicts)
            resp1 = client.get_fundamental_equity(symbol, filter_=f'Financials::Balance_Sheet::quarterly')
            resp2 = client.get_fundamental_equity(symbol, filter_=f'Financials::Income_Statement::quarterly')
            resp3 = client.get_fundamental_equity(symbol,filter_=f'Financials::Cash_Flow::quarterly')
            
            
            # Convert the responses to DataFrames
            df1 = pd.DataFrame(resp1).T
            df2 = pd.DataFrame(resp2).T
            df3 = pd.DataFrame(resp3).T
            
            
            # Ensure that there is a common key to merge on, for example, 'date' if the data is time-series
            # Replace 'common_key' with the actual key name
            
            merged_df = pd.merge(df1, df2, how='inner', on='filing_date')
            ttm_data = pd.merge(merged_df, df3, how='inner', on='filing_date')
            
            convert = [col for col in ttm_data.columns if col not in ['date_x', 'filing_date', 'currency_symbol_x', 'currency_symbol', 'date', 'date_y', 'currency_symbol_y']]
            # Convert selected columns to float
            
            
            ttm_data[convert] = ttm_data[convert].astype(float)
            
            datam = (ttm_data
                     .drop(columns=['date_y', 'currency_symbol_y','date_x', 'currency_symbol_x'])
                     .rename(columns={'netIncome_y': 'netIncome',})
                     .drop_duplicates())

            
            # ------------------------------------------------------------------------------------------------
            
            
            
            
            def get_close_price():
                url = f"https://eodhd.com/api/real-time/{symbol}?fmt=json&&api_token={api}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return float(data['close'])
                else:
                    print(f"Failed to fetch data: {response.status_code}")
                    return None
            
            close_price = get_close_price()
            
            datam = datam.set_index('date')
                        #SHARES AND ADJUSTED CLOSE PRICES
            shares = client.get_fundamental_equity(symbol,filter_=f'outstandingShares::quarterly')
            df5 = pd.DataFrame(shares).T
            convert = [col for col in df5.columns if col not in ['date', 'dateFormatted']]
            # Convert selected columns to float
            df5[convert] = df5[convert].astype(float)
            
            df5 = df5.drop('date', axis=1)
            df5 = df5.rename(columns={'dateFormatted': 'date'})
            df5 = df5.set_index('date')
            df5 = df5.sort_index(ascending=False)
            
            #ADJUSTED CLOSE PRICES
            
            resp = client.get_prices_eod(symbol, period='d', order='a', from_='1989-12-28')
            stock_data = pd.DataFrame(resp)
            stock_data.set_index('date', inplace=True)
            
            filing_dates = datam.index.tolist()
            
            
            # Convert the 'date' column in stock_data to datetime format
            stock_data.index = pd.to_datetime(stock_data.index)
            
            # Initialize an empty list to store adjusted close prices
            adjusted_close_prices = []
            
            # Iterate over each filing date
            for date in filing_dates:
                date = pd.to_datetime(date)
                # Check if the date exists in stock_data
                if date in stock_data.index:
                    adjusted_close_prices.append(stock_data.loc[date, 'adjusted_close'])
                else:
                    # Find the next available date
                    next_date = stock_data[stock_data.index > date].index.min()
                    adjusted_close_prices.append(stock_data.loc[next_date, 'adjusted_close'])
                    
            # Create a DataFrame with filing dates and their corresponding adjusted close prices
            fp = pd.DataFrame({
                'Filing Date': filing_dates,
                'Adjusted Close Price': adjusted_close_prices
            })
            
            # Display the DataFrame
            fp = (fp.rename(columns={'Filing Date': 'date'}).set_index('date'))

            #EARNINGS HISTORY
            
            ehs = client.get_fundamental_equity(symbol,filter_=f'Earnings::History')
            datahs = pd.DataFrame(ehs).T
            
            # Convert 'epsActual', 'epsEstimate', 'epsDifference', and 'surprisePercent' to float
            datahs['epsActual'] = pd.to_numeric(datahs['epsActual'], errors='coerce')
            datahs['epsEstimate'] = pd.to_numeric(datahs['epsEstimate'], errors='coerce')
            datahs['epsDifference'] = pd.to_numeric(datahs['epsDifference'], errors='coerce')
            datahs['surprisePercent'] = pd.to_numeric(datahs['surprisePercent'], errors='coerce')
            
            # Display the data types of the columns after conversion
            ehs1 = datahs.iloc[3:]
            
            # Function to calculate TTM EPS for a given date
            def calculate_ttm_eps(date, earnings_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = earnings_df.index[earnings_df.index <= date][:4]
                # Sum the epsActual values for these four quarters
                ttm_eps = earnings_df.loc[relevant_dates, 'epsActual'].sum()
                return ttm_eps
            
            # Calculate TTM EPS for each date in fp
            fp['TTM EPS'] = fp.index.map(lambda date: calculate_ttm_eps(date, ehs1))
            
            # Function to calculate TTM Revenue for a given date
            def calculate_ttm_revenue(date, revenue_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = revenue_df.index[revenue_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_revenue = revenue_df.loc[relevant_dates, 'totalRevenue'].sum()
                return ttm_revenue
            
            # Calculate TTM Revenue for each date in fp
            fp['TTM Revenue'] = fp.index.map(lambda date: calculate_ttm_revenue(date, datam))
            
            # Function to calculate TTM Revenue for a given date
            def calculate_ttm_cashflow(date, cashflow_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = cashflow_df.index[cashflow_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_cashflow = cashflow_df.loc[relevant_dates, 'totalCashFromOperatingActivities'].sum()
                return ttm_cashflow
            
            fp['TTM Cash Flow'] = fp.index.map(lambda date: calculate_ttm_cashflow(date, datam))
            
            
            def calculate_ttm_freecashflow(date, freecashflow_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = freecashflow_df.index[freecashflow_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_freecashflow = freecashflow_df.loc[relevant_dates, 'freeCashFlow'].sum()
                return ttm_freecashflow
            
            fp['TTM Free Cash Flow'] = fp.index.map(lambda date: calculate_ttm_freecashflow(date, datam))
            
            def calculate_ttm_netincome(date, netincome_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = netincome_df.index[netincome_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_netincome = netincome_df.loc[relevant_dates, 'netIncome'].sum()
                return ttm_netincome
            
            fp['TTM Net Income'] = fp.index.map(lambda date: calculate_ttm_netincome(date, datam))
            
            def calculate_ttm_totalstockequity(date, totalstockequity_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = totalstockequity_df.index[totalstockequity_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_totalstockequity = totalstockequity_df.loc[relevant_dates, 'totalStockholderEquity'].mean()
                return ttm_totalstockequity
            
            fp['TTM Total Stockholder Equity'] = fp.index.map(lambda date: calculate_ttm_totalstockequity(date, datam))
            
            def calculate_ttm_totalassets(date, totalassets_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = totalassets_df.index[totalassets_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_totalassets = totalassets_df.loc[relevant_dates, 'totalAssets'].mean()
                return ttm_totalassets
            
            fp['TTM Total Assets'] = fp.index.map(lambda date: calculate_ttm_totalassets(date, datam))
            
            def calculate_ttm_totalliab(date, totalliab_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = totalliab_df.index[totalliab_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_totalliab = totalliab_df.loc[relevant_dates, 'totalLiab'].mean()
                return ttm_totalliab
            
            fp['TTM Total Liabilities'] = fp.index.map(lambda date: calculate_ttm_totalliab(date, datam))
            
            
            def calculate_ttm_ebit(date, ebit_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = ebit_df.index[ebit_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_ebit = ebit_df.loc[relevant_dates, 'ebit'].sum()
                return ttm_ebit
            
            fp['TTM EBIT'] = fp.index.map(lambda date: calculate_ttm_ebit(date, datam))
            
            def calculate_ttm_totalcurrentliab(date, totalcurrentliab_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = totalcurrentliab_df.index[totalcurrentliab_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_totalcurrentliab = totalcurrentliab_df.loc[relevant_dates, 'totalCurrentLiabilities'].mean()
                return ttm_totalcurrentliab
            
            fp['TTM Total Current Liabilities'] = fp.index.map(lambda date: calculate_ttm_totalcurrentliab(date, datam))
            
            def calculate_ttm_grossprofit(date, grossprofit_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = grossprofit_df.index[grossprofit_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_grossprofit = grossprofit_df.loc[relevant_dates, 'grossProfit'].sum()
                return ttm_grossprofit
            
            fp['TTM Gross Profit'] = fp.index.map(lambda date: calculate_ttm_grossprofit(date, datam))
            
            
            def calculate_ttm_operatingincome(date, operatingincome_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = operatingincome_df.index[operatingincome_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_operatingincome = operatingincome_df.loc[relevant_dates, 'operatingIncome'].sum()
                return ttm_operatingincome
            
            fp['TTM Operating Income'] = fp.index.map(lambda date: calculate_ttm_operatingincome(date, datam))
            
            def calculate_ttm_sltdt(date, sltdt_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = sltdt_df.index[sltdt_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_sltdt = sltdt_df.loc[relevant_dates, 'shortLongTermDebtTotal'].mean()
                return ttm_sltdt
            
            fp['TTM Short Long Term Debt Total'] = fp.index.map(lambda date: calculate_ttm_sltdt(date, datam))
            
            def calculate_ttm_cash(date, cash_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = cash_df.index[cash_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_cash = cash_df.loc[relevant_dates, 'cash'].mean()
                return ttm_cash
            
            fp['TTM Cash'] = fp.index.map(lambda date: calculate_ttm_cash(date, datam))
            
            def calculate_ttm_shortinvestments(date, shortinvestments_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = shortinvestments_df.index[shortinvestments_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_shortinvestments = shortinvestments_df.loc[relevant_dates, 'shortTermInvestments'].mean()
                return ttm_shortinvestments
            
            fp['TTM Short Term Investments'] = fp.index.map(lambda date: calculate_ttm_shortinvestments(date, datam))
            
            def calculate_ttm_totalcurrentassets(date, totalcurrentassets_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = totalcurrentassets_df.index[totalcurrentassets_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_totalcurrentassets = totalcurrentassets_df.loc[relevant_dates, 'totalCurrentAssets'].mean()
                return ttm_totalcurrentassets
            
            fp['TTM Total Current Assets'] = fp.index.map(lambda date: calculate_ttm_totalcurrentassets(date, datam))
            
            def calculate_ttm_interestexpense(date, interestexpense_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = interestexpense_df.index[interestexpense_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_interestexpense = interestexpense_df.loc[relevant_dates, 'interestExpense'].sum()
                return ttm_interestexpense
            
            fp['TTM interest Expense'] = fp.index.map(lambda date: calculate_ttm_interestexpense(date, datam))
            
            
            def calculate_ttm_dividendspaid(date, dividendspaid_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = dividendspaid_df.index[dividendspaid_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_dividendspaid = dividendspaid_df.loc[relevant_dates, 'dividendsPaid'].sum()
                return ttm_dividendspaid
            
            fp['TTM Dividends Paid'] = fp.index.map(lambda date: calculate_ttm_dividendspaid(date, datam))
            
            def calculate_ttm_nonrecurring(date, nonrecurring_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = nonrecurring_df.index[nonrecurring_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_nonrecurring = nonrecurring_df.loc[relevant_dates, 'nonRecurring'].sum()
                return ttm_nonrecurring
            
            fp['TTM Non Recurring'] = fp.index.map(lambda date: calculate_ttm_nonrecurring(date, datam))
            
            def calculate_ttm_minorityinterest(date, minorityinterest_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = minorityinterest_df.index[minorityinterest_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_minorityinterest = minorityinterest_df.loc[relevant_dates, 'minorityInterest'].fillna(0).mean()
                return ttm_minorityinterest
            
            fp['TTM Minority Interest'] = fp.index.map(lambda date: calculate_ttm_minorityinterest(date, datam))
            
            def calculate_ttm_ebitda(date, ebitda_df):
                # Get the four quarters leading up to and including the given date
                relevant_dates = ebitda_df.index[ebitda_df.index <= date][:4]
                # Sum the totalRevenue values for these four quarters
                ttm_ebitda = ebitda_df.loc[relevant_dates, 'ebitda'].sum()
                return ttm_ebitda
            
            fp['TTM EBITDA'] = fp.index.map(lambda date: calculate_ttm_ebitda(date, datam))


            # Calculating the ratios
            historical_ratios = {}
            
            # Price Ratios
            historical_ratios['P/E'] = (fp['Adjusted Close Price'] / fp['TTM EPS'])
            historical_ratios['P/Sales'] = (fp['Adjusted Close Price'] / (fp['TTM Revenue'] / df5['shares']))
            historical_ratios['P/CF'] = (fp['Adjusted Close Price'] / (fp['TTM Cash Flow'] /  df5['shares']))
            historical_ratios['PFCF'] = (fp['Adjusted Close Price'] / (fp['TTM Free Cash Flow'] /  df5['shares']))
            historical_ratios['Free Cash Flow Yield'] = (fp['TTM Free Cash Flow'] / (fp['Adjusted Close Price'] * df5['shares']) * 100)
            
            # Profitability Ratios
            historical_ratios['Net Income Margin'] = (fp['TTM Net Income'] / fp['TTM Revenue']) * 100 
            historical_ratios['ROE'] = (fp['TTM Net Income'] / fp['TTM Total Stockholder Equity']) * 100
            historical_ratios['ROA'] = (fp['TTM Net Income'] / fp['TTM Total Assets']) * 100
            historical_ratios['ROIC'] = (fp['TTM Net Income'] / (fp['TTM Total Stockholder Equity'] + fp['TTM Total Liabilities'])) * 100
            historical_ratios['ROCE'] = (fp['TTM EBIT'] / (fp['TTM Total Assets'] - fp['TTM Total Current Liabilities'])) * 100 
            historical_ratios['Gross Margin'] = (fp['TTM Gross Profit'] / fp['TTM Revenue']) * 100
            historical_ratios['Operating Margin'] = (fp['TTM Operating Income'] / fp['TTM Revenue']) * 100 
            
            # Debt Ratios
            historical_ratios['Debt to Assets'] = (fp['TTM Short Long Term Debt Total'] / fp['TTM Total Assets']) * 100
            historical_ratios['Debt to Equity'] = (fp['TTM Short Long Term Debt Total'] / fp['TTM Total Stockholder Equity']) * 100
            historical_ratios['Cash Ratio'] = (fp['TTM Cash'] + fp['TTM Short Term Investments']) / fp['TTM Total Current Liabilities']
            historical_ratios['Current Ratio'] = fp['TTM Total Current Assets'] / fp['TTM Total Current Liabilities']
            historical_ratios['Interest Coverage'] = fp['TTM Operating Income'] / fp['TTM interest Expense'] 
            
            # Dividend Ratios
            historical_ratios['Dividend Yield'] = (fp['TTM Dividends Paid'] / df5['shares']) / fp['Adjusted Close Price'] * 100 
            historical_ratios['Payout Ratio'] = fp['TTM Dividends Paid'] / (fp['TTM Net Income'] - fp['TTM Non Recurring']) 
            
            # Other Ratios
            historical_ratios['Earnings Yield'] = fp['TTM EPS'] / fp['Adjusted Close Price'] 
            historical_ratios['EV/EBITDA'] = ((fp['Adjusted Close Price'] * df5['shares']) + fp['TTM Short Long Term Debt Total'] + fp['TTM Minority Interest'] - fp['TTM Cash']) / fp['TTM EBITDA']
            historical_ratios['EV/SALES'] = ((fp['Adjusted Close Price'] * df5['shares']) + fp['TTM Short Long Term Debt Total'] + fp['TTM Minority Interest'] - fp['TTM Cash']) / fp['TTM Revenue'] 
            historical_ratios['EV/Free Cash Flow'] = ((fp['Adjusted Close Price'] * df5['shares']) + fp['TTM Short Long Term Debt Total'] + fp['TTM Minority Interest'] - fp['TTM Cash']) / fp['TTM Free Cash Flow']            

            # Step 1: Remove duplicates from each Series index
            for key, series in historical_ratios.items():
                if series.index.duplicated().any():
                    # Keep the last occurrence of each index
                    historical_ratios[key] = series[~series.index.duplicated(keep='last')]
            
            # Step 2: Attempt to create the DataFrame again
            try:
                ratios_df = pd.DataFrame.from_dict(historical_ratios)
                # Step 3: Reverse the order of the DataFrame
                ratios_df = ratios_df.iloc[::-1]
            except ValueError as e:
                print(f"An error occurred: {e}")
            
            # Display the first few rows of the reversed DataFrame
            ratios_df = ratios_df.round(2)
            st.dataframe(ratios_df)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")






# Dictionary of pages
pages = {
    'Financial Analysis': page1,
    'Historical Multiples': page2,
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Render the selected page
if selection in pages:
    pages[selection]()
