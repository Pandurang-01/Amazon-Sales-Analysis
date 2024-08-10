#!/usr/bin/env python
# coding: utf-8

# ### Importing Nescessary Libraries 
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings(action = 'ignore')


# ### Loading The Data

# In[2]:


data = pd.read_csv('Amazon Sales data.csv')


# ### Data Undestanding

# In[3]:


data


# In[4]:


data.head()


# In[5]:


data.shape


# In[6]:


data.info()


# In[7]:


data.describe()


# In[8]:


data.columns


# In[9]:


data['Item Type'].value_counts()


# In[10]:


data['Item Type'].nunique()


# ### Data Cleaning
# 

# In[11]:


data.isnull().sum()


# ##### Since there are no null values in dataset we can move to EDA

# ### Exploratory Data Analysis

# In[12]:


data['Order Date']


# In[13]:


# Converting 'Order Date' column to datetime'

import calendar

data['Order Date'] = pd.to_datetime(data['Order Date'], format='%m/%d/%Y', errors='coerce')

# Extracting month, year, and year-month using lambda functions

data['Order Month'] = data['Order Date'].apply(lambda x: x.month if pd.notnull(x) else None)
data['Order Year'] = data['Order Date'].apply(lambda x: x.year if pd.notnull(x) else None)
data['Year-Month'] = data['Order Date'].apply(lambda x: x.to_period('M') if pd.notnull(x) else None)


# In[14]:


import calendar


data['Order Date'] = pd.to_datetime(data['Order Date'], format='%m/%d/%Y', errors='coerce')

# Extracting month and year from 'Order Date'

data['Order Month'] = data['Order Date'].dt.month

# Mapping month numbers to month names

data['Order Month'] = data['Order Month'].apply(lambda x: calendar.month_name[x])

# Group by 'Order Month' and calculate total revenue for each month

monthly_sales = data.groupby('Order Month')['Total Revenue'].sum().reset_index()


# ### Sales Trend Analysis
# 

# In[15]:


# Group by month,year,and year-month and calculating total revenue

monthly_sales = data.groupby(['Order Year', 'Order Month']).agg({'Total Revenue': 'sum'}).reset_index()

yearly_sales = data.groupby('Order Date').agg({'Total Revenue' : 'sum'}).reset_index()

yearly_monthly_sales = data.groupby('Year-Month').agg({'Total Revenue': 'sum'}).reset_index()

monthly_sales_table = pd.DataFrame(monthly_sales)

monthly_sales_table['Order Month'] = pd.Categorical(monthly_sales_table['Order Month'],
                                                    categories=calendar.month_name[1:], ordered=True)
                                                                        
monthly_sales_table = monthly_sales_table.sort_values(by = ['Order Year','Order Month'])




# In[16]:


import plotly.figure_factory as ff
 
table_fig = ff.create_table(monthly_sales_table, colorscale = 'magenta_r')
table_fig.show()


# In[17]:


# Creating subplots for each year

fig_monthly_sales = px.line(monthly_sales, x = 'Order Month', y = 'Total Revenue', color = 'Order Year',
                           title = 'Monthly Sales Trend', facet_col = 'Order Year')

# Update layout for better visulization 
 
fig_monthly_sales.update_layout(
    title = 'Monthly Sales Trend',
    xaxis_title = 'Order Month',
    yaxis_title = 'Total Revenue',
    font = dict(
        family = 'Courier New monospace',
        size = 14,
        color = 'RebeccaPurple'
    )
 )

fig_monthly_sales.show()


# In[18]:


unique_years = monthly_sales['Order Year'].unique()

# Iterating  through each year 

for year in unique_years:
    
    # Filtering the data for the current year
    
    data_year = monthly_sales[monthly_sales['Order Year'] == year]
    
    # Creating plot for the current year
    
    fig_monthly_sales = px.line(data_year, x='Order Month', y='Total Revenue', color='Order Year',
                                title=f'Monthly Sales Trend - {year}')
    
    # Updating layout for better visualization
    
    fig_monthly_sales.update_layout(
        xaxis_title="Order Month",
        yaxis_title="Total Revenue",
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="RebeccaPurple"
        )
    )
    
    fig_monthly_sales.show()


# ### Geographical Sales Analysis

# In[48]:


# Sales by different Locations

fig = px.choropleth(data, locations = 'Country',
                   color = 'Total Revenue',
                   hover_name = 'Country',
                   title = 'Total Revenue by Country')
fig.show()


# In[46]:


# Relationship between 'Country' and 'Total Revenue'

fig1 = px.bar(data, x = 'Country', y = 'Total Revenue',
              title = 'Total Revenue by Country', color='Country',)

fig1.show()


# In[50]:


# Total Revenue by Region

fig = px.bar(data, x = 'Region', y = 'Total Revenue',
             color = 'Region', title = 'Total Revenue by Region')
fig.show()


# ## Product Analysis

# In[52]:


# Category wise units Sold

fig = px.bar(data, x = 'Item Type' , y = 'Units Sold',
             color = 'Item Type',
            title = 'Units Sold by Item Type')
fig.show()


# In[59]:


# Distribution of Unit price (Price Analysi)

fig = px.histogram(data, x = 'Unit Price', nbins = 20,
                   color = 'Unit Price',
                  title = 'Distribution of Unit Price')
fig.show()


# In[55]:


# Relationship between 'Item Type' and 'Total Cost'

fig4 = px.box(data, x = 'Item Type', y = 'Total Cost',
              color = 'Item Type',
             title = 'Total Cost by Item Type',
)
fig4.show()


# In[56]:


# Relation between 'Unit Price' and 'Total Profit'

fig3 = px.scatter(data, x = 'Unit Price', y = 'Total Profit',
                  color = 'Unit Price',
                 title = 'Unit Price Vs Total profit')


fig3.show()


# In[61]:


# Profit Based on each Product Category

fig6 = px.bar(data, x = 'Item Type', y = 'Total Profit',
              color = 'Item Type',
             title = 'Total Profit by Item Type')

fig6.show()


# ### Consumer Behaviour Analysis
# 

# In[63]:


# Order Priority Analysis

fig = px.bar(data, x="Order Priority", y="Units Sold",
             color = "Order Priority",
             
            title="Units Sold by Order Priority")
fig.show()


# In[64]:


# Relationship between 'Order Priority' and 'Total Profit'

fig5 = px.bar(data, x = 'Order Priority' , y = 'Total Profit',
             title = 'Total Profit by Order Priority',
             color = 'Order Priority')

fig5.show()


# ## Sales Channel Analysis

# In[65]:


data.head()


# In[66]:


# Grouping the data by sales channel and calculating total revenue for each channel

channel_revenue = data.groupby('Sales Channel')['Total Revenue'].sum().reset_index()


# In[67]:


# Plotting the Pie

fig = px.pie(channel_revenue, values = 'Total Revenue', names = 'Sales Channel',
            title = 'Sales Distribution by Channel')

fig.show()

