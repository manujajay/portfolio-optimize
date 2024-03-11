from portfolio_optimize import PortfolioOptimize

# Define your stock tickers and parameters
tickers = ["AAPL", "MSFT", "GOOG"]
window = 5  # years of data
optimization = "MV"  # mean-variance optimization

# Initialize and run the optimizer
portfolio = PortfolioOptimize(tickers=tickers, window=window, optimization=optimization)
optimal_weights = portfolio.optimize()
print("Optimal Weights:", optimal_weights)

# Plot the efficient frontier
portfolio.graph()

# Perform and display backtesting results
portfolio.backtest()