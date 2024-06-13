#!/usr/bin/env python
# coding: utf-8

# In[32]:


import numpy as np
import pandas as pd

import datetime as dt

import warnings; warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt


# In[3]:


transactions = pd.read_csv('Transactions.csv')
customers = pd.read_csv('Customer.csv')
prod_cat_info = pd.read_csv('prod_cat_info.csv')


# In[4]:


transactions


# In[5]:


customers


# In[6]:


prod_cat_info


# # Q1 Merge the datasets Customers, Product Hierarchy and Transactions as Customer_Final. Ensure to keep all customers who have done transactions with us and select the join type accordingly.
# 
# 

# In[7]:


temp1 = pd.merge(
    left = transactions,
    right = customers,
    left_on = 'cust_id',
    right_on = 'customer_Id',
    how = 'inner'
)

Customer_Final = pd.merge(
    left = temp1,
    right = prod_cat_info,
    how = 'inner',
    left_on = ['prod_cat_code','prod_subcat_code'],
    right_on = ['prod_cat_code','prod_sub_cat_code']
             
)


# In[8]:


Customer_Final


# # Q2 Prepare a summary report for the merged data set.
#  

# ## a Get the column names and their corresponding data types

# In[9]:


Customer_Final.dtypes


# ## b Top/Bottom 10 observations

# In[10]:


Customer_Final.head(10)


# In[11]:


Customer_Final.tail(10)


# ## c “Five-number summary” for continuous variables (min, Q1, median, Q3 and max)
# 

# In[12]:


Customer_Final.describe().loc['min':,:]


# ## d Frequency tables for all the categorical variables

# In[13]:


Customer_Final.info()


# In[14]:


df = Customer_Final[['Store_type','Gender','prod_cat','prod_subcat']]

print(df['Store_type'].value_counts(),end = '\n\n\n')
print(df['Gender'].value_counts(),end = '\n\n\n')
print(df[['prod_cat','prod_subcat']].value_counts(),end = '\n\n\n')
    


# # Q3 Generate histograms for all continuous variables and frequency bars for categorical variables.

# # #histogram for continuous variables

# ## #tax

# In[34]:


plt.hist(Customer_Final.Tax)
plt.xlabel('Tax')
plt.ylabel('Frequency')

plt.show()


# ### total_amt

# In[37]:


plt.hist(Customer_Final.total_amt)
plt.xlabel('total_amt')
plt.ylabel('frequency')

plt.show()


# ## Frequency Bar for Categorical variables

# ### Gender

# In[38]:


Customer_Final['Gender'].value_counts().plot(kind = 'bar')


# ### Store_type 

# In[40]:


Customer_Final['Store_type'].value_counts().plot(kind = 'bar')


# ### product category

# In[41]:


Customer_Final['prod_cat'].value_counts().plot(kind = 'bar')


# ### Product sub category

# In[42]:


Customer_Final['prod_subcat'].value_counts().plot(kind = 'bar')


# In[ ]:





# # Q4 Calculate the following information using the merged dataset :

# ## a Time period of the available transaction data

# In[ ]:





# In[15]:


Customer_Final.trandate = pd.to_datetime(Customer_Final.tran_date)


# In[16]:


td = max(Customer_Final.trandate) - min(Customer_Final.trandate)
print('time period in days = ',td.days)


# ## b Count of transactions where the total amount of transaction was negative

# In[17]:


count = len(transactions[transactions.total_amt < 0])
print('Count of transactions where the total amount of transaction was negative =',count)


# In[ ]:





# # Q5 Analyze which product categories are more popular among females vs male customers.

# In[18]:


df = Customer_Final.drop_duplicates(subset = ['transaction_id'])
pd.pivot_table(data = df,
              index = 'prod_cat',
              columns = 'Gender',
              values = 'transaction_id',
              aggfunc = 'count')


# In[ ]:





# # Q6 Which City code has the maximum customers and what was the percentage of customers from that city?
# 

# In[19]:


df = pd.pivot_table(data = customers,
              index = 'city_code',
              values = 'customer_Id',
              aggfunc = 'count')
df = df.sort_values(by='customer_Id',ascending=False).iloc[0:1,:]

best_city_code = df.index[0]
total_customers = df.iloc[0,0]
percentage = total_customers/len(customers)

print(f'the city with max customers is {best_city_code} and count is {total_customers} and percentage is {percentage * 100}')


# In[ ]:





# # Q7 Which store type sells the maximum products by value and by quantity?

# In[20]:


df = Customer_Final.groupby('Store_type').agg({'total_amt':'sum','Qty':'sum'})
df = df.reset_index()

df = df.sort_values(by=['total_amt','Qty'],ascending = False).iloc[0]
print(df)


# In[ ]:





# # Q8 8. What was the total amount earned from the "Electronics" and "Clothing" categories from Flagship Stores?

# In[21]:


df = Customer_Final[(Customer_Final.Store_type == 'Flagship store') & (Customer_Final.prod_cat.isin(['Electronics','Clothing'])) ]
answer = df['total_amt'].sum()
answer


# In[ ]:





# # Q9 What was the total amount earned from "Male" customers under the "Electronics" category?

# In[22]:


df = Customer_Final[(Customer_Final.Gender == 'M') & (Customer_Final.prod_cat == 'Electronics')]
answer = df['total_amt'].sum()
answer


# In[ ]:





# # Q10 How many customers have more than 10 unique transactions, after removing all transactions which have any negative amounts?
# 

# In[23]:


df = Customer_Final[Customer_Final.total_amt > 0].groupby('customer_Id').agg({'transaction_id':'count'})
df[df.transaction_id > 10]


# In[ ]:





# # Q11 For all customers aged between 25 - 35, find out:

# ## a What was the total amount spent for “Electronics” and “Books” product categories?

# In[43]:


Customer_Final.DOB = pd.to_datetime(Customer_Final.DOB)
Customer_Final['Age'] = (dt.datetime.now()-Customer_Final.DOB).dt.days//365.25

df = Customer_Final[Customer_Final.Age.between (25,35)]


# In[44]:



df[(df.prod_cat == 'Books')|(df.prod_cat == 'Electronics')]['total_amt'].sum()


# ## b  What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?

# In[45]:



Customer_Final.tran_date = pd.to_datetime(Customer_Final.tran_date)


# In[46]:


Customer_Final[(Customer_Final['tran_date'] > '2014-01-01') & (Customer_Final['tran_date'] < '2014-03-01')]['total_amt'].sum()


# In[ ]:




