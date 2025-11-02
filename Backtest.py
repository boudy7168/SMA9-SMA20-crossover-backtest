#!/usr/bin/env python
# coding: utf-8

# In[5]:


import yfinance as yf
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt


# In[39]:


df=web.DataReader("AAPL","stooq","2023-01-01","2025-10-20").sort_index()
start_date="2023-01-01"
end_date="2025-10-20"
df["sma9"]=df["Close"].rolling(9).mean()
df["sma20"]=df["Close"].rolling(20).mean()
df["signal"]=np.where(df["sma9"]>df["sma20"],1,np.where(df["sma9"]<df["sma20"],-1,0))



# In[40]:


plt.figure(figsize=(10,5))
plt.plot(df["Close"],label="AAPL",color="black")
plt.plot(df["sma9"], label="SMA9",color="orange")
plt.plot(df["sma20"], label="SMA20",color="purple")
buy=(df["signal"]==1)&(df["signal"].shift(1)<=0)
sell=(df["signal"]==-1)&(df["signal"].shift(1)>=0)
plt.scatter(df.index[buy], df["Close"][buy], marker="^", color="green",label="Buy", s=60)
plt.scatter(df.index[sell], df["Close"][sell], marker="v", color="red",label="Sell", s=60)
plt.title("AAPL SM9/SMA20 crossover")
plt.legend()
plt.grid(True)
plt.show


# In[57]:


buy_prices=df.loc[buy,"Close"]
sell_prices=df.loc[sell,"Close"]
trades=pd.DataFrame({"Buy":buy_prices.values[:len(sell_prices)],"Sell":sell_prices.values})
trades["Return%"]=(trades["Sell"]-trades["Buy"])/(trades["Buy"])*100
total_return=trades['Return%'].sum()
print(trades)
print(f"total Return:{trades['Return%'].sum():.2f}% from {start_date} to {end_date}")
yearly_percentage=total_return/2
print(f"average yearly % return is {yearly_percentage:.2f}")


# In[ ]:




