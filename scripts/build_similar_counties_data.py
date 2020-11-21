#!/usr/bin/env python
# coding: utf-8

# INSTRUCTIONS: 
# Please read through the comments in this script. 
# There may be manual steps that must be taken either before or after the script executes.
# Failure to implement these manual steps may cause the script to error out.


# In[1]:


#importing necessary modules
import os

import pandas as pd
import sqlite3


# In[2]:


#creating and connecting to sqlite database
conn = sqlite3.connect(os.path.join("data", "similar_counties.sqlite"))
cur = conn.cursor()


# In[3]:


#reading in raw data output by our clustering algorithm (cluster.py)
#run the following commented code once within cluster.py, 
#just after the 'names' and 'neighbors_ind' objects have been created to get them into a csv
#temp_df = pd.concat([names, pd.DataFrame(neighbors_ind)], axis=1)
#temp_df.to_csv("neighbors.csv")
data = pd.read_csv(os.path.join("data", "neighbors.csv"))


# In[4]:


#creating an empty list
transformed_data = []

#going through each row of the raw data
#each row represents a county
#each county has its 5 most similar counties listed on the same row
#looping and pulling out each similar county onto a separate row
for row in data.iterrows():
    for i in range(1,6):
        to_append = [str(row[1]["combined_fips"]).zfill(5), str(data.iloc[row[1][str(i)]]["combined_fips"]).zfill(5), i]
        transformed_data.append(to_append)

#renaming columns
transformed_df = pd.DataFrame(transformed_data, columns=["combined_fips","similar_combined_fips","rank"])


# In[6]:


#sql query to create a table
create_table = """create table if not exists similar_counties (
combined_fips text,
similar_combined_fips text,
rank int)
"""


# In[7]:


#creating the table
cur.execute(create_table)


# In[8]:


#appending the transformed data to the table
transformed_df.to_sql("similar_counties", conn, if_exists="append", index=False)


# In[9]:


#commiting changes and closing connection
conn.commit()
conn.close()


# In[5]:


#a preview of what the data looks like
transformed_df.head(30)


# In[ ]:




