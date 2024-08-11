# src/model_evaluation.py

import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.statespace.structural import UnobservedComponents
from statsmodels.tsa.api import VAR
from math import sqrt

# Load the preprocessed data (using relative path)
df = pd.read_csv('../data/EURUSD_daily.csv', index_col='Unnamed: 0')
df.index = pd.to_datetime(df.index)

# Sort the index to ensure it's monotonic
df = df.sort_index()

# Create a complete date range
all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

# Reindex the DataFrame to include all dates
df = df.reindex(all_dates)

# Interpolate missing values (using linear interpolation)
for col in df.columns:
    df[col] = df[col].interpolate(method='linear')

# Set the frequency of the index to daily
df.index.freq = 'D'

# Split the data into training and testing sets
train_data = df[:-30]  # Use all but the last 30 days for training
test_data = df[-30:]   # Use the last 30 days for testing

# --- State-Space Model ---
# Extract the closing price as the time series
close_price_train = train_data['4. close']
close_price_test = test_data['4. close']

# Create the local level model using UnobservedComponents
ss_model = UnobservedComponents(close_price_train, 
                                 level='local level', 
                                 stochastic_level=False) 

# Fit the model
ss_results = ss_model.fit()

# Get out-of-sample predictions
ss_predictions = ss_results.get_prediction(start=len(close_price_train), 
                                           end=len(df)-1)

# --- VAR Model ---
# Select the relevant columns for the VAR model
var_data_train = train_data[['4. close', '2. high', '3. low']]
var_data_test = test_data[['4. close', '2. high', '3. low']]

# Create the VAR model
var_model = VAR(var_data_train)

# Fit the model
var_results = var_model.fit(maxlags=10)

# Get out-of-sample predictions
var_predictions = var_results.forecast(var_data_train.values[-10:], steps=len(test_data))
var_predictions = pd.DataFrame(var_predictions, index=test_data.index, columns=var_data_test.columns)

# --- Evaluate Models ---
# Calculate RMSE and MAE for both models
models = ['State-Space', 'VAR']
rmse = []
mae = []

for model_name, predictions in zip(models, [ss_predictions.predicted_mean, var_predictions['4. close']]):
    rmse.append(sqrt(mean_squared_error(close_price_test, predictions)))
    mae.append(mean_absolute_error(close_price_test, predictions))

# Create a DataFrame to display the results
results_df = pd.DataFrame({'Model': models, 'RMSE': rmse, 'MAE': mae})
print(results_df)