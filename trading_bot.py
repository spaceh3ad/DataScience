import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
plt.style.use('ggplot')

df = pd.read_csv('pyrobot/tsla.csv', parse_dates=True, index_col=0)

# calculate 3 moving averages
# short/fast moving expo
shortEMA = df.Close.ewm(span=5, adjust=False).mean()

# med expo moving averg
midEMA = df.Close.ewm(span=21, adjust=False).mean()

# calculate long/slow moving aver
longEMA = df.Close.ewm(span=63, adjust=False).mean()

df['shortEMA'] = shortEMA
df['midEMA'] = midEMA
df['longEMA'] = longEMA

def buy_sell(data):
    buy = []
    sell = []
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):
        if data['midEMA'][i] > data['longEMA'][i] and data['shortEMA'][i] < data['midEMA'][i] and flag_long == False and flag_short == False:
            buy.append(data['Adj Close'][i])
            sell.append(np.nan)
            flag_short = True
        
        elif flag_short == True and data['shortEMA'][i] > data['midEMA'][i]:
            sell.append(data['Adj Close'][i])
            buy.append(np.nan)
            flag_short = False

        elif data['midEMA'][i] > data['longEMA'][i] and data['shortEMA'][i] > data['midEMA'][i] and flag_long == False and flag_short == False:
            buy.append(data['Adj Close'][i])
            sell.append(np.nan)
            flag_long = True
        
        elif flag_long == True and data['shortEMA'][i] < data['midEMA'][i]:
            sell.append(data['Adj Close'][i])
            buy.append(np.nan)
            flag_long = False
        
        else:
            buy.append(np.nan)
            sell.append(np.nan)
    
    return (buy,sell)
        
a = buy_sell(df)
df['Buy'] = a[0]
df['Sell']= a[1]

#calculate profit
def calc_profit(invest_capital, data):
    profit = 0
    profit_ = invest_capital
    profit_arr = [] 
    profit_aggr = []

    for i in range(0, len(data)):

        if df['Buy'][i] == df['Buy'][i]:
            print('Money investing: {}'.format(profit_))
            print('Bought: {} actions for {} | stock_price: {}'.format(round((profit_/df['Buy'][i]), 4), round(profit_, 4), round(df['Buy'][i], 4)))
            actions = profit_/df['Buy'][i]
            buff = 0
            profit = 0
        
        elif df['Sell'][i] == df['Sell'][i]:
            buff = actions*df['Sell'][i]
            print('Sold: {} actions for {} | stock_price: {}'.format(round(actions, 4), round(buff, 4), round(df['Sell'][i], 4)))

            profit = buff - profit_
            profit_ += profit


            print('profit from this operation: {} | total_profit: {}'.format(profit, profit_ -100))
            print()

        else:
            buff = 0
        
        profit_arr.append(round(profit_, 10))
        profit_aggr.append(profit_)

    return profit_arr, profit_aggr

df['profit'], df['aggr_profit'] = calc_profit(1000, df)
 

fig, ax = plt.subplots()
ax.ticklabel_format(style='plain')

ax.plot(df.index, df['profit'], label='profit $$$', color='magenta', alpha=0.35)
ax.plot(df.index, df['Adj Close'], label='Adj Close', color='blue', alpha=0.35)
ax.scatter(df.index, df['Buy'], label='BUY', marker='^', color='green', alpha=1)
ax.scatter(df.index, df['Sell'], label='SELL', marker='v', color='red', alpha=1)
plt.legend(loc='upper left')

plt.show()
