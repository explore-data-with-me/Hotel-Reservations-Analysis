#!/usr/bin/env python
# coding: utf-8

# # importing libraries

# In[ ]:





# In[59]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # loading the datasets

# In[125]:


df = pd.read_csv(r"F:\End_to_End Projects\python\datasets\hotel_bookings 2.csv")


# # exploratory data analysis and data analysis 

# In[126]:


df.head()


# In[127]:


df.shape


# In[128]:


df.columns


# In[129]:


df.info()


# In[ ]:





# In[ ]:





# In[130]:


df.info()


# In[131]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%d/%m/%Y')


# In[132]:


df.info()


# In[133]:


df.describe(include = 'object')
#### to get statostical data pf string columns 


# In[134]:


### to see these different types in these object or string datatype columns

for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print("-"*50)


# In[135]:


df['hotel'].unique()
### you can use unique function wih any column seperately as well


# In[136]:


df.isnull().sum()


# In[137]:


#### droping the columns which are not of any use and has null values as well
df.drop(['company','agent'],axis = 1, inplace = True)


# In[138]:


df.isnull().sum()


# In[139]:


### now we will drop the rows which has null value in column

df.dropna(inplace = True)


# In[140]:


df.isnull().sum()


# In[141]:


df.describe()


# ## now in above description you can see there are a lot of outliers like take children column it shows max children are 10 which is a very rare case so it is an outlier although we won't focus on it this at all because for this project we have assumed initially that we don't have any outliers
# 

# # but we will focus on outlier in the column adr(average daily rate)...there is too much gap between min and max... so we would have to remove it

# In[142]:


df = df[df['adr']<5000]


# In[143]:


df.describe()


# In[ ]:





# # 2nd step :  performing analysis and visualizations

# In[144]:


cancelled = df['is_canceled'].value_counts()


# In[145]:


cancelled


# In[146]:


cancelled_percent = df['is_canceled'].value_counts(normalize = True)
cancelled_percent
### to get the percentage


# # now we can see that cancelation rate is almost 38% which is very high and a issue we need to resolve

# In[147]:


print(cancelled_percent)

plt.figure(figsize = (5,4))   ## setting the size of the plot
plt.title('Reservation status count') # setting the title of the plot.
plt.bar(['Not Canceled','Canceled'],df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)
plt.show()


# In[ ]:





# # now we will check which hotel has what cancellation rate

# In[148]:


plt.figure(figsize =(8,4))
ax1 = sns.countplot(x = 'hotel' , hue = 'is_canceled', data = df, palette = 'Blues')
plt.title('Reservation status in different hotels' , size = 20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not canceled','canceled'])
plt.show()
                    
                    


# In[112]:


"""
plt.figure(figsize =(8,4))
ax1 = sns.countplot(x = 'hotel' , hue = 'is_canceled', data = df, palette = 'Blues')
plt.title('Reservation status in different hotels' , size = 20)
legend_labels,_ = ax1. get_legend_handle_labels()
ax1.legend(bbox_to_anchor(1,1))
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not canceled','canceled'])
plt.show()



how the above statement was shown in the video
"""


# In[149]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize= True)


# In[150]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize= True)


# In[ ]:





# In[ ]:





# In[151]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[152]:


plt.figure(figsize = (20,8))
plt.title('Average Daily Rates in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# # now calculating who has higher rates most of the time

# In[153]:


# Calculate average daily rates for resort and city hotels
average_adr_resort = resort_hotel['adr'].mean()
average_adr_city = city_hotel['adr'].mean()

# Determine which hotel type has higher average daily rates most of the time
if average_adr_resort > average_adr_city:
    higher_rate_hotel = 'Resort Hotel'
elif average_adr_resort < average_adr_city:
    higher_rate_hotel = 'City Hotel'
else:
    higher_rate_hotel = 'Both Resort and City Hotels have the same average daily rates'

print("Hotel with higher average daily rates most of the time:", higher_rate_hotel)


# In[154]:


# Calculate average daily rates for resort and city hotels
average_adr = [average_adr_resort, average_adr_city]
hotel_types = ['Resort Hotel', 'City Hotel']

# Plotting the bar graph
plt.figure(figsize=(8, 6))
plt.bar(hotel_types, average_adr, color=['blue', 'green'])
plt.title('Average Daily Rates of Resort and City Hotels')
plt.xlabel('Hotel Type')
plt.ylabel('Average Daily Rate')
plt.show()


# In[ ]:





# In[155]:


# Calculate total average daily rate
total_average_adr = average_adr_resort + average_adr_city

# Calculate percentages
percentage_resort = (average_adr_resort / total_average_adr) * 100
percentage_city = (average_adr_city / total_average_adr) * 100

# Plotting the bar graph
plt.figure(figsize=(8, 6))
plt.bar('Resort Hotel', percentage_resort, color='blue', label='Resort Hotel')
plt.bar('City Hotel', percentage_city, color='green', label='City Hotel', bottom=percentage_resort)
plt.title('Percentage of Average Daily Rates by Hotel Type')
plt.xlabel('Hotel Type')
plt.ylabel('Percentage')
plt.legend()

# Adding percentage labels on top of bars
plt.text('Resort Hotel', percentage_resort + 1, f'{percentage_resort:.1f}%', ha='center', va='bottom', fontsize=10, color='black')
plt.text('City Hotel', percentage_resort + percentage_city / 2 + 1, f'{percentage_city:.1f}%', ha='center', va='bottom', fontsize=10, color='black')

plt.show()


# In[ ]:





# #  now lets find out which month has higher cancellation rates

# In[ ]:





# In[156]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'bright')
plt.title('Reservation status per Month', size = 20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled', 'canceled'])
plt.show()


# # highest cancelation rate is in january month and lowest in august
# # lets find the reasons for the above

# In[ ]:





# In[121]:


"""     now we are finding the average daily rates per month so that we can fimd out is the reson for more cancellation
in month of january is because of rates in that month or not          """


# In[157]:


plt.figure(figsize = (15,8))
plt.title('ADR per Month', fontsize = 30)
sns.barplot(x='month',y='adr',data =df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# ## yeah we can see that the rates are highest in the month of january so it can be the potential reason behind the more cancellation rates in this month
# ## but it is not the only factor because as we can see month of august does not have lowest prices  but it still has lowest cancelation rates

# In[ ]:





# # now lets find top 10 countries which has maximum cancellation rates

# In[ ]:





# In[158]:


cancelled_data = df[df['is_canceled'] == 1]  ### only taking cancelled rows by doing this
top_10_country = cancelled_data['country'].value_counts()[:10]   #### now kind of grouping those rows by country and then taking only first 10 by writing this [:10]

plt.figure(figsize = (8,8))
plt.title('Top 10 Countries with Reservation Cancelled')
plt.pie(top_10_country, autopct='%.2f', labels = top_10_country.index)  ## plotting pie then need to check this label function properly , where and how can be it used.
plt.show()


# ### so we can see most of the cancellation is being done in the portugal country.  so we suggest that , hotels there needs to increase their facilities , do maintainence regulary and provide some discount offers as well

# In[ ]:





# # now lets find out where the clients are coming from, online or offline travel agents or others

# In[ ]:





# In[159]:


df['market_segment'].value_counts()


# In[160]:


df['market_segment'].value_counts(normalize = True)


# In[161]:


cancelled_data['market_segment'].value_counts(normalize = True)


# ## now our original hypothesis that says more customers are from offline bookings prove to be wrong here and in cancellation too online segment takes the lead

# In[ ]:





# ### now the reason can be the hotels in reality does not match their photos on their websites and are of poor quality.

# In[ ]:





# ## now lets check the prices of reservations which has been cancelled compared to the reservations which has not been cancelled 
# 

# In[163]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

not_cancelled_data = df[df['is_canceled'] == 0]
not_cancelled_df_adr =not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace = True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize=(20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not_cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend()


# In[166]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']>'2017-09')]

not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']>'2017-09')]


# In[167]:


plt.figure(figsize=(20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not_cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend()


# ## make the above chart acc to video

# In[ ]:





# ## cancelled rate is higher than the non cancelled rate .that means we can say price is directly proportional to cancellation rate. higher the price , higher the chances of cancellation

# In[ ]:





# In[ ]:





# In[47]:


for col in df.columns:
    print(col)
    print(df[col].unique())
    print("-"*50)


# In[ ]:




