# src/data_preprocessing.py

import configparser
import requests
import pandas as pd

# Read the API key from the config file
config = configparser.ConfigParser()
config.read('../config/config.ini')
api_key = config['alpha_vantage']['api_key']

# Symbol for EUR/USD currency pair
symbol = 'EURUSD'

# Alpha Vantage API endpoint
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full'

# Make the API request
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Extract the time series data
    time_series = data['Time Series (Daily)']
    # Convert to a pandas DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)

    # Save the preprocessed data to a CSV file
    df.to_csv('../data/EURUSD_daily.csv')

    print(f'Data saved to data/EURUSD_daily.csv')
else:
    print(f'Error fetching data: {response.status_code}')