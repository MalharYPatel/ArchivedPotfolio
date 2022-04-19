# -*- coding: utf-8 -*-
'''EDA of Market Sectors
Created on Thu Mar  3 09:22:03 2022

@author: Malhar

First We Download the following ETF data
Energy: XLE
Materials: XLB
Industrials: XLI
Consumer Discretionary: XLY
Consumer Staples: XLP
Health Care: XLV
Financials: XLF
Information Technology: XLK

Communication Services: VOX
or possibly SPDR XTL OR
iShares U.S. Telecommunications IYZ OR
FSTCX mutual fund

Utilities: XLU
Real Estate: FSRPX mutual fund


import yfinance as yf
import pandas as pd
import numpy as np
data = yf.download("XLE XLB XLI XLY XLP XLV XLF XLK VOX XLU FSRPX", interval='1mo', start="1995-01-01", end="2022-01-01")
df = pd.DataFrame(data)
df.to_csv("D:\\SectorSelect.csv")
'''

#First we import the data, clear empty rows,
#and correctly format the dtypes, and make a useful list for later
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

etflist = ['XLE', 'XLB', 'XLI', 'XLY', 'XLP', 'XLV', 'XLF', 'XLK', 'VOX', 'XLU', 'FSRPX']

df = pd.read_csv("D:\Malhar\\Anaconda3\\Malhar\\Data\\SectorSelect.csv")
df = df.dropna()
tempdate = pd.to_datetime(df['Date'])
df = df.drop(['Date'], axis = 1)
df = df.astype(float)
#df.plot()
df.insert(loc=0,column='Date', value=tempdate) 


#Now we insert decimal change numbers for every etf, for 1, 3, 6 and 12 months
for e in etflist:
    op = e+".O"
    cl = e+".C"
    one_month = e+"1M"
    three_month = e+"3M"
    six_month = e+"6M"
    twelve_month = e+"12M"
    df[one_month] = ((df[cl]-df[op])/100)
    df[three_month] = ((df[cl]-df[op].shift(2))/100)
    df[six_month] = ((df[cl]-df[op].shift(5))/100)
    df[twelve_month] = ((df[cl]-df[op].shift(11))/100)
#and again remove the NaN rows
df = df.dropna()

#Now for some correlations, 1M, 3M, 6M, 12M, and autocorrelation
#first we make lists of the data sections we need
one_M = []
three_M = []
six_M = []
twelve_M = []
for e in etflist:
    a = e+"1M"
    one_M.append(a)
    a = e+"3M"
    three_M.append(a)
    a=e+"6M"
    six_M.append(a)
    a=e+"12M"
    twelve_M.append(a)
'''   
#next we make the correlation plots
plt.figure()
plot = sns.heatmap(data = df[one_M].corr(), cmap = 'rainbow')
plt.figure()
plot2 = sns.heatmap(data = df[three_M].corr(),cmap = 'rainbow')
plt.figure()
plot3 = sns.heatmap(data = df[six_M].corr(), cmap = 'rainbow')
plt.figure()
plot4 = sns.heatmap(data = df[twelve_M].corr(), cmap = 'rainbow')
#and we use a loop to get individual autocorrelation plots
for e in one_M:
    plt.figure()
    plot = pd.plotting.autocorrelation_plot(df[e])
    plot.set_xlim([0, 24])
    plot.set_ylim([-0.25, 0.25])
    plt.title(e)
 
'''

#We can assess the mean return of each equity over the above lookback periods
'''
templist = one_M + three_M+six_M+twelve_M
df2 = df[templist].copy().mean().reset_index()
df2 = pd.DataFrame(df2)
df2.columns = ['ETF','Mean']
df2['Mean'] = df2['Mean'] * 100 
print(df2.head())
sns.set(rc = {'figure.figsize':(15,8)}) # this changes the size of the plot to make it larger
sns.barplot(data = df2, x = 'ETF', y = 'Mean')
plt.xticks(rotation = -90)
plt.ylim(0,9.5)

df2 = df2.sort_values(by = 'Mean')
plt.figure()
sns.barplot(data = df2, x = 'ETF', y = 'Mean', palette = 'pastel')
plt.xticks(rotation = -90)
plt.ylim(0,9.5) 
'''

    
#We can assess the Standard deviation of each equity over the above lookback periods
'''
templist = one_M + three_M+six_M+twelve_M
df2 = df[templist].copy().std().reset_index()
df2 = pd.DataFrame(df2)
df2.columns = ['ETF','StdDev']
print(df2.head())
plt.ylim(0,0.16)
plt.xticks(rotation = -90)
sns.barplot(data = df2, x = 'ETF', y = 'StdDev')
df2 = df2.sort_values(by = 'StdDev')
plt.figure()
plt.ylim(0,0.16)
plt.xticks(rotation = -90)
sns.barplot(data = df2, x = 'ETF', y = 'StdDev', palette = 'dark')    
'''

#And now metrics for risk adjusted return [return / StDev]
'''
templist = one_M + three_M+six_M+twelve_M
df2 = df[templist].copy().std().reset_index()
df2 = pd.DataFrame(df2)
df3 = df[templist].copy().mean().reset_index()
df3 = pd.DataFrame(df3)
df2.columns = ['ETF','StdDev']
df3.columns = ['ETF','Mean']
df2['Mean'] = df3['Mean']*100
df2['RaR'] = df2['Mean']/df2['StdDev']
print(df2.head())
plt.clf()
plt.figure()
plt.ylim(0,80)
plt.xticks(rotation = -90)
sns.barplot(data = df2, x = 'ETF', y = 'RaR')
plt.show()
df2 = df2.sort_values(by = 'RaR')

plt.clf()
plt.figure()
plt.ylim(0,80)
plt.xticks(rotation = -90)
sns.barplot(data = df2, x = 'ETF', y = 'RaR', palette = 'dark')
'''

#Making a bar graph and boxplot of average monthly return by etf
#We start by making a new variable which has the one_M values converted to %s
'''
one_MS  = df[one_M] * 100
sns.set(rc = {'figure.figsize':(15,8)}) # this changes the size of the plot to make it larger
plot = sns.boxplot(data = one_MS)
plt.xticks(rotation=90) 
plt.yticks(np.arange(-2.5,2.7,0.25))
plot.set_ylim(-2.5,2.7)
plt.figure()
plot2 = sns.barplot(data = one_MS, ci = None)
plot2 = sns.barplot(data = one_MS)
''' 


#To create a chart of what each etf returns for each calender month
#we make a copy, create a month column, and make a pivot table, then give the index names
df_M = df.copy()
df_M['Month'] = pd.to_datetime(df_M['Date']).dt.strftime('%d') #used d instead of m due to UK formatting
monthly_pivot = pd.pivot_table(data = df_M, values= one_M, index= 'Month', aggfunc=lambda x: stats.trim_mean(x, 0.1))
monthly_pivot = monthly_pivot.reset_index()
months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_pivot['Month'] = months_list
monthly_pivot[one_M] *= 100 
'''
print(monthly_pivot.head())
sns.set(rc = {'figure.figsize':(15,8)})
for e in one_M:
    plt.figure()
    plt.title(e)
    sns.barplot(data = monthly_pivot[['Month',e]], x=monthly_pivot['Month'], y = e)
'''


#and a swarm plot to show the return of each etf per month

df_M = df.copy()
df_M['Month'] = pd.to_datetime(df_M['Date']).dt.strftime('%d') #used d instead of m due to UK formatting
df_1 = pd.pivot_table(data = df_M, values= one_M, index= 'Month', aggfunc=lambda x: stats.trim_mean(x, 0.1))
months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_1['Month'] = months_list
df_1[one_M] *= 100 
df1 = df_1.melt(id_vars='Month', var_name='ETF name', value_name='Value')


df_M = df.copy()
df_M['Month'] = pd.to_datetime(df_M['Date']).dt.strftime('%d') #used d instead of m due to UK formatting
df_3 = pd.pivot_table(data = df_M, values= three_M, index= 'Month', aggfunc=lambda x: stats.trim_mean(x, 0.1))
months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_3['Month'] = months_list
df_3[three_M] *= 100 
df3 = df_3.melt(id_vars='Month', var_name='ETF name', value_name='Value')



df_M = df.copy()
df_M['Month'] = pd.to_datetime(df_M['Date']).dt.strftime('%d') #used d instead of m due to UK formatting
df_6 = pd.pivot_table(data = df_M, values= six_M, index= 'Month', aggfunc=lambda x: stats.trim_mean(x, 0.1))
months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_6['Month'] = months_list
df_6[six_M] *= 100 
df6 = df_6.melt(id_vars='Month', var_name='ETF name', value_name='Value')

df_M = df.copy()
df_M['Month'] = pd.to_datetime(df_M['Date']).dt.strftime('%d') #used d instead of m due to UK formatting
df_12 = pd.pivot_table(data = df_M, values= twelve_M, index= 'Month', aggfunc=lambda x: stats.trim_mean(x, 0.1))
months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_12['Month'] = months_list
df_12[twelve_M] *= 100 
df12 = df_12.melt(id_vars='Month', var_name='ETF name', value_name='Value')

sns.set_style('white')
sns.set(rc = {'figure.figsize':(20,11)})
plt.figure()
sns.swarmplot(data = df1, x='Month', y = 'Value', hue = 'ETF name', palette = 'terrain' )
plt.tight_layout()
plt.figure()
sns.swarmplot(data = df3, x='Month', y = 'Value', hue = 'ETF name', palette = 'Spectral' )
plt.tight_layout()
plt.figure()
sns.swarmplot(data = df6, x='Month', y = 'Value', hue = 'ETF name', palette = 'rocket' )
plt.tight_layout()
plt.figure()
sns.swarmplot(data = df12, x='Month', y = 'Value', hue = 'ETF name', palette = 'Spectral_r' )
plt.tight_layout()
