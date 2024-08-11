import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents
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
df['4. close'] = df['4. close'].interpolate(method='linear')

# Set the frequency of the index to daily
df.index.freq = 'D'

# Extract the closing price as the time series
close_price = df['4. close']

# Create the local level model using UnobservedComponents
model = UnobservedComponents(close_price, 
                             level='local level', 
                             stochastic_level=False) 

# Fit the model
results = model.fit()

# Print the model summary
print(results.summary())

# Get in-sample predictions (fitted values)
predictions = results.get_prediction(start=0, end=len(close_price)-1)

# Plot the actual vs. predicted values
plt.figure(figsize=(10, 6))
close_price.plot(label='Actual')
predictions.predicted_mean.plot(label='Predicted', alpha=0.7)
plt.legend()
plt.title('EUR/USD Closing Price - Local Level Model')
plt.show()