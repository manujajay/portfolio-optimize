import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from tqdm.auto import tqdm

class PortfolioOptimize:
    def __init__(self, tickers, window=5, optimization='MV'):
        """
        Initializes the portfolio optimization class.

        Parameters:
        - tickers: List of stock tickers to include in the portfolio.
        - window: The number of years of historical data to consider for optimization.
        - optimization: The type of optimization to perform ('MV' for mean-variance).
        """
        self.tickers = tickers
        self.window = window
        self.optimization = optimization
        self.weights = None
        self.returns = None
        self.cov_matrix = None
        self.data = None
        self.risk_free_rate = None

    def fetch_risk_free_rate(self):
        """Fetches the current risk-free rate using the 13-week Treasury bill rate (^IRX) as a proxy."""
        print("Fetching the current risk-free rate...")
        treasury_ticker = '^IRX'
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365 * self.window)
        treasury_data = yf.download(treasury_ticker, start=start_date, end=end_date)['Adj Close']
        # Convert the average annual yield to a daily rate
        self.risk_free_rate = treasury_data.mean() / 100 / 252
        print("Risk-free rate fetched.")


    def fetch_data(self):
        """Fetches historical stock data for the given tickers."""
        print("Fetching historical stock dat