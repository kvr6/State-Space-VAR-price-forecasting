# src/var_model.py

import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

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

# Select the relevant columns for the VAR model
# (You can choose other columns or create new features)
data = df[['4. close', '2. high', '3. low']]

# Create the VAR model
model = VAR(data)

# Fit the model (you can specify the lag order using the 'maxlags' parameter)
results = model.fit(maxlags=10)  # Example: Use a maximum of 10 lags

# Print the model summary
print(results.summary())

# Get in-sample predictions (fitted values)
predictions = results.fittedvalues

# Plot the actual vs. predicted values for the closing price
plt.figure(figsize=(10, 6))
plt.plot(df.index, data['4. close'], label='Actual')
plt.plot(predictions.index, predictions['4. close'], label='Predicted', alpha=0.7)
plt.legend()
plt.title('EUR/USD Closing Price - VAR Model')
plt.show()