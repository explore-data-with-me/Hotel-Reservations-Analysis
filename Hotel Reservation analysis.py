#!/usr/bin/env python
# coding: utf-8

# # importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# # Loading the datasets
df = pd.read_csv(r"F:\End_to_End Projects\python\datasets\hotel_bookings 2.csv")

# # Exploratory data analysis and data analysis 

df.head()
df.shape
df.columns
df.info()

df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%d/%m/%Y')

df.info()

df.describe(include = 'object')
#### to get statistical data pf string columns 

### to see these different types in these object or string datatype columns

for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print("-"*50)

df['hotel'].unique()
### You can use a unique function with any column separately as well

df.isnull().sum()

#### dropping the columns which are not of any use and have null values as well
df.drop(['company','agent'],axis = 1, inplace = True)

df.isnull().sum()

### Now we will drop the rows that have null values in the column

df.dropna(inplace = True)

df.isnull().sum()

df.describe()


# ## Now in the above description you can see there are a lot of outliers take the children column it shows max children is 10 which is a very rare case so it is an outlier although we won't focus on this at all because for this project we have assumed initially that we don't have any outliers

# # but we will focus on the outlier in the column ADR(average daily rate)...there is too much gap between min and max... so we would have to remove it

df = df[df['adr']<5000]

df.describe()

# # 2nd step:  performing analysis and visualizations

cancelled = df['is_canceled'].value_counts()

cancelled_percent = df['is_canceled'].value_counts(normalize = True)

### to get the percentage


# # Now we can see that the cancelation rate is almost 38% which is very high and an issue we need to resolve

print(cancelled_percent)

plt.figure(figsize = (5,4))   ## setting the size of the plot
plt.title('Reservation status count') # setting the title of the plot.
plt.bar(['Not Canceled','Canceled'],df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)
plt.show()

# # Now we will check which hotel has what cancellation rate

plt.figure(figsize =(8,4))
ax1 = sns.countplot(x = 'hotel' , hue = 'is_canceled', data = df, palette = 'Blues')
plt.title('Reservation status in different hotels' , size = 20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not canceled','canceled'])
plt.show()
                    

resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize= True)

city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize= True)

resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()

plt.figure(figsize = (20,8))
plt.title('Average Daily Rates in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# # Now calculating who has higher rates most of the time

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

# Calculate the total average daily rate
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

# #  now lets find out which month has higher cancellation rates

df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'bright')
plt.title('Reservation status per Month', size = 20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled', 'canceled'])
plt.show()


# # The highest cancelation rate is in January month and the lowest in August
# # Let's find the reasons for the above

"""     now we are finding the average daily rates per month so that we can find out the reason for more cancellation
in the month of January is because of rates in that month or not          """

plt.figure(figsize = (15,8))
plt.title('ADR per Month', fontsize = 30)
sns.barplot(x='month',y='adr',data =df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# ## Yeah we can see that the rates are highest in the month of January so it can be the potential reason behind the higher cancellation rates in this month
# ## but it is not the only factor because as we can see the month of August does not have the lowest prices  but it still has lowest cancelation rates

# # Now let's find the top 10 countries which have maximum cancellation rates

cancelled_data = df[df['is_canceled'] == 1]  ### only taking cancelled rows by doing this
top_10_country = cancelled_data['country'].value_counts()[:10]   #### now kind of grouping those rows by country and then taking only the first 10 by writing this [:10]

plt.figure(figsize = (8,8))
plt.title('Top 10 Countries with Reservation Cancelled')
plt.pie(top_10_country, autopct='%.2f', labels = top_10_country.index)  ## plotting pie then need to check this label function properly, where and how can be it used.
plt.show()


# ### so we can see most of the cancellations are being done in the Portuguese country.  so we suggest that hotels there need to increase their facilities, do maintenance regularly and provide some discount offers as well

# # Now let's find out where the clients are coming from, online or offline travel agents or others

df['market_segment'].value_counts()

df['market_segment'].value_counts(normalize = True)

cancelled_data['market_segment'].value_counts(normalize = True)

# ## Now our original hypothesis that says more customers are from offline bookings proves to be wrong here and in cancellation too online segment takes the lead

# ### Now the reason can be the hotels in reality do not match the photos on their websites and are of poor quality.

# ## Now let's check the prices of reservations which has been canceled compared to the reservations which have not been canceled 

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

cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']>'2017-09')]

not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']>'2017-09')]

plt.figure(figsize=(20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label = 'not_cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label = 'cancelled')
plt.legend()

# ## canceled rate is higher than the non-canceled rate That means we can say the price is directly proportional to the cancellation rate. higher the price , higher the chances of cancellation
