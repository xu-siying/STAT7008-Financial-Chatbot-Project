import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = "sp500_index.csv"  # 文件路径
data = pd.read_csv(file_path)

# 转换日期格式
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 计算每日涨跌幅
data['Daily Change (%)'] = ((data['Close'] - data['Open']) / data['Open']) * 100

# 计算高低价差
data['High-Low Spread'] = data['High'] - data['Low']

# 计算移动平均线
data['MA_30'] = data['Close'].rolling(window=30).mean()
data['MA_90'] = data['Close'].rolling(window=90).mean()

# 绘制收盘价趋势图
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.6)
plt.plot(data.index, data['Adj Close'], label='Adj Close Price', color='orange', alpha=0.6)
plt.plot(data.index, data['MA_30'], label='30-Day MA', color='green', linestyle='--')
plt.plot(data.index, data['MA_90'], label='90-Day MA', color='red', linestyle='--')
plt.title("S&P 500 Index Close Price Trend")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# 绘制成交量柱状图
plt.figure(figsize=(14, 7))
plt.bar(data.index, data['Volume'], color='purple', alpha=0.6)
plt.title("S&P 500 Index Daily Volume")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.grid()
plt.show()

# 绘制高低价差图
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['High-Low Spread'], label='High-Low Spread', color='brown', alpha=0.6)
plt.title("S&P 500 Index High-Low Spread")
plt.xlabel("Date")
plt.ylabel("Price Spread")
plt.grid()
plt.show()

# 绘制每日涨跌幅分布
plt.figure(figsize=(10, 6))
plt.hist(data['Daily Change (%)'].dropna(), bins=50, color='cyan', alpha=0.7)
plt.title("Daily Change (%) Distribution")
plt.xlabel("Daily Change (%)")
plt.ylabel("Frequency")
plt.grid()
plt.show()