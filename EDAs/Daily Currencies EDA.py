# -*- coding: utf-8 -*-
#import the relevant libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
#read in the relevant data. Note that due to \ causing conflict with python
#for some of the filepaths, rawstring r could to be used, or \\
audusd = pd.read_csv("D:\Malhar\Anaconda3\Malhar\Data\AUDUSD.csv")
eurusd = pd.read_csv("D:\Malhar\Anaconda3\Malhar\Data\EURUSD.csv")
gbpusd = pd.read_csv("D:\Malhar\Anaconda3\Malhar\Data\GBPUSD.csv")
nzdusd = pd.read_csv("D:\Malhar\Anaconda3\Malhar\Data\\NZDUSD.csv")
usdcad = pd.read_csv(r"D:\Malhar\Anaconda3\Malhar\Data\USDCAD.csv")
usdchf = pd.read_csv("D:\Malhar\Anaconda3\Malhar\Data\\USDCHF.csv")
usdjpy = pd.read_csv("D:\Malhar\Anaconda3\Malhar\Data\\USDJPY.csv")


Currencies = (audusd, eurusd, gbpusd, nzdusd, usdcad, usdchf, usdjpy)

audusd.name = 'AUDUSD'
eurusd.name =  'EURUSD'
gbpusd.name=  'GBPUSD'
nzdusd.name = 'NZDUSD'
usdcad.name = 'USDCAD'
usdchf.name = 'USDCHF'
usdjpy.name = 'USDJPY'






#Basic info
for c in Currencies:
    print(c.head(5))
    print(c.info())
#nzdusd has one value missing compared to the others


#Trim outliers from the datasets, esp USDCHF

#Convert all times to pandas Datetimes,using UK format
for c in Currencies:
    c['Gmt time'] = pd.to_datetime(c['Gmt time'], dayfirst=True)
    c = c.rename(columns={'Gmt time': 'Date'}, inplace = True)

  

#Since this is a time series, replace missing values with averages
for c in Currencies:
    c = c[{'Open','High','Low','Close','Volume'}].fillna(c.mean())

#Add in columns for % daily change(return) and %daily movement(volatility)
for c in Currencies:
    c['%Change'] = 100*((c['Close'] - c['Open']) / c['Open'])
    c['%Move'] = 100*((c['High'] - c['Low']) / c['Open'])




#Mean Value Plots
meanval = pd.DataFrame(['AUDUSD', 'EURUSD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'], columns=['Currency'])
Av_Percent_Change = []
Av_Percent_Move = []
Av_Vol = []
for c in Currencies:
     Av_Percent_Change.append(c['%Change'].mean())
     Av_Percent_Move.append(c['%Move'].mean())
     Av_Vol.append(c['Volume'].mean())
meanval['Average % Change'], meanval['Average % Move'], meanval['Average Volume']  =  Av_Percent_Change,  Av_Percent_Move , Av_Vol
print(meanval)

sns.set_style('darkgrid')
sns.despine()
plt.xticks(rotation=-90) 
sns.barplot(x = meanval['Currency'], y = meanval['Average % Change'], palette= 'coolwarm' )
plt.show()
plt.clf()
sns.barplot(x = meanval['Currency'], y = meanval['Average % Move'], palette= 'cool')
plt.show()
plt.clf()
sns.barplot(x = meanval['Currency'], y = meanval['Average Volume'], palette= 'pastel')
plt.show()


#Day of Week Plots
sns.set_style('darkgrid')
sns.despine()
for c in Currencies:
    c['DayofWeek'] = c['Date'].dt.day_name()
    sns.barplot(data = c, x='DayofWeek', y ='%Change', palette='pastel')#showfliers = False
    plt.axhline(c['%Change'].mean())
    plt.title(c.name)
    plt.show()
    plt.clf()

#Month of Year Plots
sns.set_style('darkgrid')
sns.despine()
for c in Currencies:
    c['Month'] = c['Date'].dt.month_name()
    sns.barplot(data = c, x='Month', y ='%Change', palette='cool' )
    plt.axhline(c['%Change'].mean())
    plt.title(c.name)
    plt.xticks(rotation=-45)
    plt.show()
    plt.clf()
    
'''

for c in Currencies:
    c['MonthofWeek'] = c['Date'].dt.month_name()
    sns.lineplot(data = c, x='MonthofWeek', y ='%Change', palette='cool' )
    plt.axhline(0)
    plt.xticks(rotation=-45)
plt.show()






Misc code
data = stats.trim_mean(data, 0.1)


#Autocorrelation Plots
for c in Currencies:
    ax= pd.plotting.autocorrelation_plot(c['%Change'])
    ax.set_xlim([0,365])
    ax.set_ylim([-0.07,0.06])
    plt.title(c.name)
    plt.show()
    plt.clf()

'''

'''


sns.set_style('darkgrid')
sns.despine()
fig, axes = plt.subplots(1,3)
sns.barplot(x = meanval['Currency'], y = meanval['Average % Change'], palette= 'coolwarm', ax=axes[0])
sns.barplot(x = meanval['Currency'], y = meanval['Average % Move'], palette= 'cool', ax=axes[1])
sns.barplot(x = meanval['Currency'], y = meanval['Average Volume'], palette= 'pastel', ax=axes[2])



audusd = audusd.rename(columns={'Gmt time': 'Date'})
audusd['Date'] = pd.to_datetime(audusd['Date'])
eurusd = eurusd.rename(columns={'Gmt time': 'Date'})
eurusd['Date'] = pd.to_datetime(eurusd['Date'])
gbpusd = gbpusd.rename(columns={'Gmt time': 'Date'})
gbpusd['Date'] = pd.to_datetime(gbpusd['Date'])
nzdusd = nzdusd.rename(columns={'Gmt time': 'Date'})
nzdusd['Date'] = pd.to_datetime(nzdusd['Date'])
usdcad = usdcad.rename(columns={'Gmt time': 'Date'})
usdcad['Date'] = pd.to_datetime(usdcad['Date'])
usdchf = usdchf.rename(columns={'Gmt time': 'Date'})
usdchf['Date'] = pd.to_datetime(usdchf['Date'])
usdjpy = usdjpy.rename(columns={'Gmt time': 'Date'})
usdjpy['Date'] = pd.to_datetime(usdjpy['Date'])

#Since this is a time series, replace missing values with averages
audusd = audusd.fillna(audusd.mean())
eurusd = audusd.fillna(audusd.mean())
gbpusd = audusd.fillna(audusd.mean())
nzdusd = audusd.fillna(audusd.mean())
usdcad = usdcad.fillna(usdcad.mean())
usdchf = usdcad.fillna(usdcad.mean())
usdjpy = usdcad.fillna(usdcad.mean())

#Basic info on files
print(audusd.head(5))
print(eurusd.head(5))
print(gbpusd.head(5))
print(nzdusd.head(5))
print(usdcad.head(5))
print(usdchf.head(5))



audusd.info()
eurusd.info()
gbpusd.info()
nzdusd.info()
usdcad.info()
usdchf.info()
usdjpy.info()

#meanval.insert(loc=1, column= 'Av% Change', value=Av_Percent_Change)
#meanval.insert(loc=1, column= 'Av% Move', value=Av_Percent_Move)
'''


