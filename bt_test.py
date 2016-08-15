The MIT License (MIT)
Copyright (c) <2016> <Julian Gilyard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class Stock:
    equity = ''
    percent = 0.0
    cash = 0.0
    ret = 0.0
    
    def sp(self):
        print self.percent, 
        print " ",
        print self.equity,
        print " ",
        print self.cash

import json
import csv
import pandas as pd
from pprint import pprint
import sys
import matplotlib.pyplot as plt
import numpy as np
#252 trading days
num_bt_days = int(sys.argv[2]) * 252
principle = int(sys.argv[1])
num_years = int(sys.argv[2])
if(int(sys.argv[2]) >3):
    print "argument larger than 3"
    sys.exit(0)

#allocates Data points array for backtest

with open('output.json') as data_file:    
    data = json.load(data_file)
#pprint(data)

num_boon = len(data['boonPercentOut'])
num_stocks = len(data['customPercentOut'])


stock_holder =[Stock] * (num_boon + num_stocks)
for x in range(0,(num_boon +num_stocks)):
    stock_holder[x] = Stock()
    
print(len(stock_holder))
runner =0
holder = Stock()
for x in range(0,num_boon):
    stock_holder[runner].equity = (data['boonPercentOut'][x]['symbol'])
    stock_holder[runner].percent = (data['boonPercentOut'][x]['percent'])
    runner = runner +1
    

for x in range(0,num_stocks):
    stock_holder[runner].equity = holder.equity
    stock_holder[runner].percent = (data['customPercentOut'][x]['percent'])
    stock_holder[runner].equity = (data['customPercentOut'][x]['symbol'])
    runner = runner +1

#holds Panada Df for Stocks of Ten Years
historical_data = [None] * (runner)

for i in range(0,runner):
    df = pd.read_csv(stock_holder[i].equity + '.csv')
    column = df.ix[:,6]
    dates = df.Date
    historical_data[i] = column

df_comp = pd.read_csv("SP_500.csv")
comp = df_comp.Close
comp_points = [float] * len(comp)
plot_comp = [float] * num_bt_days
for i in range(0,len(comp)):
    comp_points[i] = float(comp[i])
money_comp = principle
for i in range(0, num_bt_days):
    comp_diff = comp_points[(num_bt_days -i)-1] - comp_points[(num_bt_days-i)]
    comp_diff = comp_diff / comp_points[(num_bt_days -1)]
    comp_diff = float(comp_diff)
    delta  = float(comp_diff)
    money_comp = money_comp* (1 + delta)
    plot_comp[i] = money_comp
    #print(comp[(num_bt_days -i)])

cash_port = [float] * runner
print "Portfolio Allocation"
for i in range(0,runner):
    cash_port[i] = (float(stock_holder[i].percent) / 100) *principle
    stock_holder[i].cash = cash_port[i]
print "%   Equity    $"
TCH = 0.0
for x in range (0,runner):
    stock_holder[x].sp()
    TCH = stock_holder[x].cash +TCH
print "Total Cash Holdings", 
print TCH
print "Number of Days for Back Test",
print num_bt_days
data_points = [float] * num_bt_days
daily_returns = [float] * (int(sys.argv[2]) * 252)
num_months =  (int(sys.argv[2]) * 252)
money_holder = [float] * runner 
for i in range (0,num_bt_days):
    #because calloc doesnt exist...
    data_points[i] = 0.0
for i in range(0,num_bt_days):
    
    for j in range(0,runner):
        first = historical_data[j]
        second = historical_data[j]
        delta = second[(num_bt_days-i) -1] - first[(num_bt_days -i)]
        delta = delta/second[(num_bt_days -i)]
        stock_holder[j].cash = float(stock_holder[j].cash * (1 + delta))
    for k in range(0,runner):
        temp = data_points[i]
        data_points[i] = float(stock_holder[k].cash) + temp
#compute Sharpe Ratio with respect to the risk free rate....
for i in range(0,num_months):
    #monthly_returns[i] = (data_points[(i*(num_bt_days/num_months))] - data_points[0]) / data_points[0]
    daily_returns[i] = (data_points[i] - data_points[0]) / data_points[0] -.0271
#sharpe Ratio
s_ratio = np.average(daily_returns)/np.std(daily_returns)
print "Sharpe Ratio",
print s_ratio
print "Average Annual Returns",
average_returns = (data_points[num_bt_days -1] - data_points[0]) / data_points[0]
average_returns = average_returns / int(sys.argv[2])
print average_returns

#adjusted 20 adjusted to one year
loss_returns = .20/5 * num_years

SFratio = (average_returns -loss_returns)/np.std(daily_returns)
print "SFratio ajusted over average returns",
print SFratio

plt.plot(data_points,'r')
plt.plot(plot_comp,'b')
plt.show()
plt.savefig('output.png')
