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
        print("Fetching historical stock data...")
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365 * self.window)
        self.data = yf.download(self.tickers, start=start_date, end=end_date)['Adj Close']
        print("Stock data fetched.")


    def calculate_expected_returns_and_cov(self):
        """Calculates expected returns and the covariance matrix for the stocks."""
        print("Calculating expected returns and covariance matrix...")
        returns = self.data.pct_change().dropna()
        self.returns = returns.mean()
        self.cov_matrix = returns.cov()
        print("Calculations completed.")

    def optimize(self):
        """
        Optimizes the portfolio to maximize the Sharpe ratio, which is the ratio of
        excess return to volatility.
        """
        print("Starting portfolio optimization...")
        if self.data is None:
            self.fetch_data()
        if self.risk_free_rate is None:
            self.fetch_risk_free_rate()
        self.calculate_expected_returns_and_cov()

        num_assets = len(self.tickers)
        bounds = tuple((0.0, 1.0) for asset in range(num_assets))

        def objective(weights):
            port_return = np.dot(weights, self.returns) * 252
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights))) * np.sqrt(252)
            sharpe_ratio = (port_return - self.risk_free_rate) / port_volatility
            return -sharpe_ratio  # We minimize the negative Sharpe ratio to maximize it

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1},)
        initial_guess = num_assets * [1. / num_assets,]

        result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        self.weights = result.x
        print("Optimization completed.")
        return dict(zip(self.tickers, self.weights))

    def graph(self):
        """
        Plots the efficient frontier for the portfolio. The efficient frontier shows
        the highest expected return for a given level of risk.
        """
        if self.cov_matrix is None or self.returns is None:
            print("You must optimize the portfolio before plotting.")
            return
        
        print("Plotting the efficient frontier...")
        num_portfolios = 10000
        results = np.zeros((3, num_portfolios))

        for i in tqdm(range(num_portfolios), desc="Simulating portfolios"):
            weights = np.random.random(len(self.tickers))
            weights /= np.sum(weights)
            port_return = np.dot(weights, self.returns) * 252
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights))) * np.sqrt(252)
            sharpe_ratio = (port_return - self.risk_free_rate) / port_volatility
            results[0,i] = port_volatility
            results[1,i] = port_return
            results[2,i] = sharpe_ratio
        
        plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='viridis')
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Volatility (Standard Deviation)')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier')
        plt.show()

    def portfolio_performance(self, weights):
        """
        Calculates the performance of the portfolio based on the given weights.
        
        Returns the portfolio's expected annual return, volatility, and Sharpe ratio.
        """
        print("Calculating portfolio performance...")
        port_return = np.dot(weights, self.returns) * 252
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights))) * np.sqrt(252)
        sharpe_ratio = (port_return - self.risk_free_rate) / port_volatility
        return port_return, port_volatility, sharpe_ratio

    def backtest(self):
        """
        Simulates historical performance of the optimized portfolio, plots the cumulative returns,
        and calculates key performance metrics.
        """
        if self.weights is None:
            print("Optimization must be completed before backtesting.")
            return

        # Calculate daily returns of the portfolio
        daily_returns = self.data.pct_change()
        portfolio_daily_returns = daily_returns.dot(self.weights)

        # Calculate cumulative returns
        cumulative_returns = (1 + portfolio_daily_returns).cumprod()

        # Plot cumulative returns
        plt.figure(figsize=(10, 6))
        cumulative_returns.plot()
        plt.title('Portfolio Cumulative Returns')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.show()

        # Performance metrics
        total_return = cumulative_returns.iloc[-1] - 1
        annualized_return = np.power(cumulative_returns.iloc[-1], 252 / len(portfolio_daily_returns)) - 1
        annualized_volatility = portfolio_daily_returns.std() * np.sqrt(252)
        sharpe_ratio = (annualized_return - self.risk_free_rate) / annualized_volatility

        # Display performance metrics
        print(f"Total Return: {total_return:.2%}")
        print(f"Annualized Return: {annualized_return:.2%}")
        print(f"Annualized Volatility: {annualized_volatility:.2%}")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")


# Example usage
tickers = ["AAPL", "MSFT", "GOOG"]
portfolio = PortfolioOptimize(tickers=tickers, window=5, optimization='MV')
optimal_weights = portfolio.optimize()
print("Optimal Weights:", optimal_weights)
portfolio.graph()
