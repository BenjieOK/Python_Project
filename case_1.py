import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import quandl
# Get attendees to get their own key.
quandl.ApiConfig.api_key = 'gYyp7CLTPWqhbsyFNAN2'

# Select a basket of stocks to work with. They can pick their own.
selected = ['CNP', 'F', 'WMT', 'GE', 'TSLA']

# Get the data from Quandl for these stock
data = quandl.get_table('WIKI/PRICES', ticker=selected,
                        qopts={'columns': ['ticker', 'date', 'adj_close']},
                        date={'gte': '2014-1-1', 'lte': '2016-12-31'},
                        paginate=True
                        )


clean = data.set_index('date')
table = clean.pivot(columns='ticker')

# What's our data look like now?
print(table.head())


returns_daily = table.pct_change()
returns_annual = returns_daily.mean()*250
returns_annual
print(returns_annual)


# Get the daily covariance of returns of the stock.
# This is effectively, how much does one stock deviate from the mean.
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

# Read this table as....
# If all your stock if F (facebook), you'd get 6% volatility
# (variance from the mean) over the year.
# If you had 50% F (facebook) and 50% (GE), you'd get 2% volatility
# (variance from the mean) over the year.
cov_annual
print(cov_annual)


# Now calculate the efficient frontier - over 50,000 permutations of the stocks

port_returns = []
port_volatility = []
stock_weights = []

num_assets = len(selected)
num_portfolios = 50000

# Set a random seed, for reprodicibility
np.random.seed(101)

for p in range(num_portfolios):

    # Calculate a random weight, and make it a percentage of
    # all the weights calculated for this basket.
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)

    # Calculate the returns for this weighting of stocks,
    # using the annual returns
    returns = np.dot(weights, returns_annual)

    # Calculate the volatility for this weighting of stocks,
    # using the annual coveriance values
    # Effictively std. deviation
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))

    # Store the values for this portfolio
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

# Add a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns, 'Volatility': port_volatility}

# Extend the dictionary, to accomdate each ticker and weight in the portfolio
for counter, symbol in enumerate(selected):
    portfolio[symbol + ' Weight'] = [Weight[counter]
                                     for Weight in stock_weights]

# Finally! Make a DataFrame...
df = pd.DataFrame(portfolio)

# What's our data look like?
df.head()
print(df.head())

# Visualize the frontier!
# Use a scatter plot, and use seaborn colour styling...
plt.style.use('seaborn')
df.plot.scatter(x='Volatility', y='Returns', figsize=(10, 8), grid=True)
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()


# Now introduce the sharpe ratio.
#
#   ratio = Rp - Rfp
#           --------
#              ap
#
# Rp = Expected Reward (we have this)
# Rfp = Risk-Free Reward (we have a value of 0 for this)
# ap = Risk (Volatility) - we have this.


port_returns = []
port_volatility = []
stock_weights = []
# THIS IS NEW
sharpe_ratio = []

num_assets = len(selected)
num_portfolios = 50000

# Set a random seed, for reprodicibility
np.random.seed(101)

for p in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))

    # THIS IS NEW
    ratio = returns/volatility

    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

    # THIS IS NEW
    sharpe_ratio.append(ratio)

# THIS HAS AN EXTRA VALUE
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

for counter, symbol in enumerate(selected):
    portfolio[symbol + ' Weight'] = [Weight[counter]
                                     for Weight in stock_weights]

df = pd.DataFrame(portfolio)

df.head()
print(df.head())

# Plot the efficient frontier, but this time, use a heatmap to colour code
# based on the sharpe ratio...

plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns',  c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()


# Now, figure out what the max profit is we could get...
max_sharpe = df['Sharpe Ratio'].max()
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]

# And figure out the most risk-averse portfolio...
min_volatility = df['Volatility'].min()
min_volatility_portfolio = df.loc[df['Volatility'] == min_volatility]

# Plot these as extra points on the graph...

plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns',  c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)

# These are new compared to the previous plot...
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'],
            c='red', marker='D', s=200)

plt.scatter(x=min_volatility_portfolio['Volatility'],
            y=min_volatility_portfolio['Returns'],
            c='blue', marker='D', s=200)

plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()

# Finally, to get the specifics of the two portfolios,
# print them out...

print(min_volatility_portfolio.T*100)
print(sharpe_portfolio.T*100)

# Most risk-adverse person would get 4.5% returns,
# with a calculated volatility of 13.8%.
# The best returns available are 11.6%
# with a volatility of 17.6%.
