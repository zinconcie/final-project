# -*- coding: utf-8 -*-

# -- Project --

# # Final Project - Analyzing Sales Data
# 
# **Date**: 12 January 2023
# 
# **Author**: Manarin Sukcharoen (Manar)
# 
# **Course**: `Pandas Foundation`


# import data
import pandas as pd
df = pd.read_csv("sample-store.csv")

# preview top 5 rows
df.head()

# shape of dataframe
df.shape

# see data frame information using .info()
df.info()

# We can use `pd.to_datetime()` function to convert columns 'Order Date' and 'Ship Date' to datetime.


# example of pd.to_datetime() function
pd.to_datetime(df['Order Date'].head(), format='%m/%d/%Y')

# TODO - convert order date and ship date to datetime in the original dataframe
df.reset_index()

# TODO - count nan in postal code column
df['Postal Code'].isna().sum()

# TODO - filter rows with missing values
df[df['Postal Code'].isna()]

# TODO - Explore this dataset on your owns, ask your own questions

# ## Data Analysis Part
# 
# Answer 10 below questions to get credit from this course. Write `pandas` code to find answers.


# TODO 01 - how many columns, rows in this dataset
df.shape

# TODO 02 - is there any missing values?, if there is, which colunm? how many nan values?
df.isna().sum()

# TODO 03 - your friend ask for `California` data, filter it and export csv for him
csv1 = df[df['State']=='California']
csv1.to_csv("california.csv")

# TODO 04 - your friend ask for all order data in `California` and `Texas` in 2017 (look at Order Date), send him csv file
df['Order Date'] = pd.to_datetime(df['Order Date'],format='%m/%d/%Y')
csv2 = df[(df['Order Date'].dt.year == 2017) & (df['State']=='California')|(df['State']=='Texas') ]
csv2.to_csv('California_texas_2017.csv')

# TODO 05 - how much total sales, average sales, and standard deviation of sales your company make in 2017
df[df['Order Date'].dt.year == 2017]['Sales'].agg(['sum','mean','std']).round(2).reset_index()


# TODO 06 - which Segment has the highest profit in 2018
df[df['Order Date'].dt.year == 2018].groupby('Segment')['Profit'].sum().sort_values(ascending = False)

# TODO 07 - which top 5 States have the least total sales between 15 April 2019 - 31 December 2019
df['Order Date'] = pd.to_datetime(df['Order Date'],format='%m/%d/%Y')
df_range = df.loc[(df['Order Date'] >= '2019-04-15') & (df['Order Date'] <'2019-12-31')].groupby('State')['Sales'].sum().sort_values().head(5)
print (df_range)

# TODO 08 - what is the proportion of total sales (%) in West + Central in 2019 e.g. 25% 

df['Order Date'] = pd.to_datetime(df['Order Date'],format='%m/%d/%Y')
df_sale = df[df['Order Date'].dt.year == 2019].groupby('Region')['Sales'].sum().reset_index()
df_sale['%'] = (100* df_sale['Sales']/df_sale['Sales'].sum()).round(2)
ans = df_sale.loc[df_sale['Region'].isin(['West', 'Central']), '%'].sum()
print (ans)

# TODO 09 - find top 10 popular products in terms of number of orders vs. total sales during 2019-2020


df['Order Date'] = pd.to_datetime(df['Order Date'],format='%m/%d/%Y')
df2 = df.loc[(df['Order Date'].dt.year >= 2019) & (df['Order Date'].dt.year <= 2020)]

print ("\n Top 10 product in terms of number of orders during 2019-2020")
product = pd.DataFrame(df2.value_counts('Product Name').sort_values(ascending = False).head(10).reset_index())
product.columns = ['Product Name','Total orders']
print(product)


print ("\n Top 10 product in terms of total sales during 2019-2020")
sales = pd.DataFrame(df2.groupby('Product Name')['Sales'].sum().sort_values(ascending = False).round(2).head(10).reset_index())
sales.columns = ['Product Name','Total Sales']
print(sales)



# TODO 10 - plot at least 2 plots, any plot you think interesting :)
import matplotlib as mpl
import matplotlib.pyplot as plt

df.groupby('Ship Mode')['Quantity'].sum()\
.plot.pie(y='Ship Mode',  figsize=(5,5), autopct='%1.1f%%', startangle=90)\
.set_title('Table 1  = Show the percentage of ship mode calculated by quantity')
plt.show()


df['Year'] = df['Order Date'].dt.strftime('%Y')
table =pd.DataFrame( df.groupby(['Year','Region'])['Profit'].sum().reset_index())
df.groupby(['Year','Region']).size().unstack().plot(kind='bar', stacked=True)
plt.xlabel("Year")
plt.ylabel("Profit")
plt.title('Table 1  = Show the correlation between region and profit during year 2017-2020', size = 15)
plt.show()   

# TODO Bonus - use np.where() to create new column in dataframe to help you answer your own questions

#Question = Which state have overdue when shipping period = 5 days?
import numpy as np
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')
df['Date_diff'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Check'] = np.where(df['Date_diff'] <= 5 ,"Passed","Overdue")
df.groupby(['State','Check'])['Date_diff'].size().unstack().plot(kind='area', stacked=True)

