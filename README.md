# State-Space Models and VAR for Price Forecasting

## Description

This repository explores the application of state-space models and Vector Autoregression (VAR) for forecasting prices in financial markets, specifically the EUR/USD exchange rate. It provides a practical implementation of these techniques using Python and the `statsmodels` library.

## Methodology

* **State-Space Models:** State-space models provide a framework for modeling time series data by representing the underlying system as a set of hidden states and observations. This repository uses a local level model, which assumes a slowly changing underlying trend (level) and random noise.
* **Vector Autoregression (VAR):** VAR models are used to analyze the relationships between multiple time series variables. They are suitable for understanding the interconnectedness of different markets and forecasting their future values.

**Steps:**

1. **Data Preprocessing:** Load the EUR/USD daily price data, sort the date index, fill missing values using linear interpolation, and set the frequency to daily.
2. **Model Training:** Train both the state-space and VAR models on the preprocessed data. The VAR model uses a maximum lag order of 10, allowing the model to select the optimal lag order based on information criteria.
3. **Model Evaluation:** Evaluate the performance of both models using Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE) on a hold-out test set (the last 30 days of data).
4. **Visualization:** Create a plot comparing the actual EUR/USD closing prices to the forecasts from both models.

## Data

* **Source:** Alpha Vantage API (https://www.alphavantage.co/)
* **Description:** This project uses historical daily price data for the EUR/USD currency pair obtained from the Alpha Vantage API. The data includes open, high, low, and close prices, as well as volume.
* **API Key:** You will need to obtain a free API key from Alpha Vantage to access the data. Instructions on how to obtain an API key can be found on their website. 

## Usage

1. **Clone the repository:** `git clone [repository_url]`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Configure API Key:**
    - Create a file named `config.ini` in the `config/` directory.
    - Add the following content to the file, replacing `YOUR_API_KEY` with your actual API key:

    ```ini
    [alpha_vantage]
    api_key = YOUR_API_KEY
    ```

    **Important:** Do not commit the `config.ini` file to the repository. Add it to your `.gitignore` file to prevent it from being accidentally uploaded. 

4. **Run the scripts (from the root directory of the project):**
    * `python src/data_preprocessing.py`
    * `python src/state_space_model.py`
    * `python src/var_model.py`
    * `python src/model_evaluation.py`
    * `python src/visualization.py`

## Dependencies

* `statsmodels`
* `pandas`
* `numpy`
* `matplotlib`
* `sklearn`

## Results

* **Model Performance:** The VAR(10) model outperformed the local level state-space model on the out-of-sample test data, achieving lower RMSE and MAE values. This suggests that the VAR model, by leveraging multiple variables and lagged relationships, is better able to capture the dynamics of the EUR/USD exchange rate.
* **State-Space Model:** The local level model captured the long-term trend well but was less responsive to short-term fluctuations and trend changes.
* **VAR Model:** The VAR model was more responsive to short-term price movements and better captured periods of high volatility. However, it is more complex and might be prone to overfitting if not carefully tuned.

## Visualization

The `visualization.py` script generates a plot comparing the actual EUR/USD closing prices to the forecasts from both models. The plot visually confirms the superior performance of the VAR model in tracking the actual price movements, particularly during periods of volatility and trend changes.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

[Choose a license and add it here, e.g., MIT License]