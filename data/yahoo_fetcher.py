import yfinance as yf
import pandas as pd

# Define a list of NIFTY 50 stock symbols
nifty50_symbols = ['TCS.NS', 'HDFCBANK.NS', 'RELIANCE.NS', ...]  # Add all NIFTY 50 symbols

# Define the date range for historical data
start_date = '2022-01-01'
end_date = '2023-01-01'

# Create a DataFrame to store historical data
historical_data = pd.DataFrame()

# Download historical data for each stock
for symbol in nifty50_symbols:
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    historical_data[symbol] = stock_data['Adj Close']

# Save the data to a CSV file
historical_data.to_csv('nifty50_historical_data.csv')

print("Historical data downloaded and saved.")