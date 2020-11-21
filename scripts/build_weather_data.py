#!/usr/bin/env python
# coding: utf-8

# INSTRUCTIONS: 
# Please read through the comments in this script. 
# There may be manual steps that must be taken either before or after the script executes.
# Failure to implement these manual steps may cause the script to error out.

# In[29]:


#importing necessary modules
import os

import pandas as pd
import sqlite3


# In[94]:


#reading in data that was taken from this site: https://www.currentresults.com
#the site aggregated data from NOAA
#we chose to get data from this site as opposed to NOAA directly via api because NOAA's newest api limits requests to 1,000-10,000 per day
#currentresults had already aggregated decades worth of data (~1970s to ~2010)
#though even a few degrees difference is significant in terms of climate,
#for our purposes of giving an indication of temperatures that might be expected throughout the year this data was sufficient

#for temperature data
#copy and paste the data into a spreadsheet
#use a vlookup to add state fips
#delete columns "State" and "Avg C"
#calculate the percentiles using the 'PERCENTRANK.INC()' function in excel
#rename the columns 'state_fips', 'avg_x_temp', 'avg_x_temp_rank', 'avg_x_temp_percentile'
#replace x in the columns names with the current time period, e.g. 'winter'
#save as csv

#for sunny days data
#copy and paste the data into a spreadsheet
#use a vlookup to add state fips
#delete columns "State", "Place", "% Sun" and "Total Hours"
#calculate the percentiles using the 'PERCENTRANK.INC()' function in excel
#rename the columns 'state_fips', 'avg_sunny_days', 'avg_sunny_days_rank', 'avg_sunny_days_percentile'
#save as csv

#change the target csv and dtype names for each of the following
#avg_annual_temp.csv, avg_fall_temp.csv, avg_spring_temp.csv, avg_summer_temp.csv, avg_winter_temp.csv, avg_sunny_days.csv
data = pd.read_csv(os.path.join("data", "avg_winter_temp.csv"), dtype={"state_fips":str, 
                                                "avg_winter_temp":float,
                                                "avg_winter_temp_rank":int,
                                                "avg_winter_temp_percentile":float})
#state fips should have leading 0s if only 1 digit long
data["state_fips"] = data["state_fips"].apply(lambda x: x.zfill(2))
data.head(10)


# In[101]:


#query to create tables
#update table name and column names accordingly to match the name of the target csv being run currently
#avg_annual_temp.csv, avg_fall_temp.csv, avg_spring_temp.csv, avg_summer_temp.csv, avg_winter_temp.csv, avg_sunny_days.csv
create_table = """create table if not exists avg_winter_temp (
state_fips text primary key,
avg_winter_temp real,
avg_winter_temp_rank int,
avg_winter_temp_percentile real)
"""

#query to get data from table
#update table name accordingly
query_table = """select * from avg_winter_temp"""

#query to see all current tables in the database
see_tables = """select name from sqlite_master where type='table'"""


# In[96]:


#creating and connecting to the database
conn = sqlite3.connect(os.path.join("data", "weather_data.sqlite"))
# conn = sqlite3.connect("market_maven.sqlite")
cur = conn.cursor()


# In[97]:


#creating table
cur.execute(create_table)


# In[98]:


#adding data to table
data.to_sql("avg_winter_temp", conn, if_exists="append", index=False)


# In[99]:


#checking to make sure data was added correctly
cur.execute(query_table)
rows = cur.fetchall()
rows


# In[100]:


#commit changes and close connection
conn.commit()
conn.close()

