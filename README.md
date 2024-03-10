# Portfolio Optimize

A simple Python package for optimizing investment portfolios using historical return data from Yahoo Finance. Users can easily determine the optimal portfolio allocation among a given set of tickers based on the mean-variance optimization method or other algorithms.

## Features

- Easy-to-use interface for defining a portfolio of tickers.
- Supports customization of the data window (in years) for historical data analysis.
- Allows choosing between mean-variance optimization and other optimization algorithms.
- Includes functionality to plot the efficient frontier for the selected portfolio.

## Installation

```
pip install portfolio-optimize
```

## Usage

### Portfolio Optimization

```python
from portfolio_optimize.portfolio_optimize import PortfolioOptimize

# Initialize the optimizer
portfolio = PortfolioOptimize(tickers=["MSFT", "AAPL", "GOOG"], window=5, optimization="MV")

# Optimize the portfolio
optimal_weights = portfolio.optimize()

print(optimal_weights)
```

### Plotting the Efficient Frontier

```python
# Assuming you've already created and optimized the `portfolio` as shown above

# Plot the efficient frontier for the set of tickers
portfolio.graph()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is provided for educational purposes only. It is not intended for financial, investment, trading, or any other type of professional advice. Use at your own risk. The author(s) and contributors do not accept any responsibility for any decisions or actions taken based on the use of this software. Always conduct your own research and consult with financial advisors before making any investment decisions.

## Contributing

This project is under ongoing development, and contributions, corrections, and improvements are welcome. Please feel free to open issues or pull requests on [GitHub](https://github.com/manujajay/portfolio-optimize/tree/main) if you have suggestions or code enhancements.
