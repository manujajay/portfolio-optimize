from portfolio_optimize.portfolio_optimize import PortfolioOptimize

# Define your parameters directly
tickers = ["AAPL", "MSFT", "GOOG"]
window = 5  # years
optimization = "MV"  # Mean-Variance Optimization

# Initialize, optimize, and plot in a few lines
portfolio = PortfolioOptimize(tickers=tickers, window=window, optimization=optimization)
optimal_weights = portfolio.optimize()
print("Optimal Weights:", optimal_weights)
portfolio.graph()
