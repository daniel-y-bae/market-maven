#!/usr/bin/env python
# coding: utf-8

# INSTRUCTIONS: 
# Please read through the comments in this script. 
# There may be manual steps that must be taken either before or after the script executes.
# Failure to implement these manual steps may cause the script to error out.


# In[11]:


import requests
import pandas as pd
import os
import numpy as np
print('Working directory:\n' + os.getcwd())


# # Geog reference

# In[ ]:


#state & county
df_counties = pd.read_excel(os.path.join('data', 'all-geocodes-v2019.xlsx'), header=4)
df_counties = df_counties.rename(columns={'State Code (FIPS)': 'state_fips', 'County Code (FIPS)': 'county_fips', 'Area Name (including legal/statistical area description)':'county_name'})
df_counties = df_counties[(df_counties['county_fips']!=0) & (df_counties['Summary Level']==50) & (df_counties['state_fips']<= 56)]
df_counties = df_counties[['county_fips', 'state_fips', 'county_name']]
#display(df_counties)

#state to division to region
'''
This file has a list of stacked census-defined states, regions, and divisions
'''
df_s_d_r = pd.read_excel(os.path.join('data', 'state-geocodes-v2019.xlsx'), header=5)
df_s_d_r = df_s_d_r.rename(columns={'State (FIPS)': 'state_fips', 'Division':'division_cd', 'Region':'region_cd', 'Name':'name'})

#regions
df_regions = df_s_d_r[(df_s_d_r['state_fips']==0) & (df_s_d_r['division_cd']==0)]
df_regions = df_regions.rename(columns={'name':'region_name'})
df_regions = df_regions[['region_cd', 'region_name']]

#divisions
df_divisions = df_s_d_r[(df_s_d_r['state_fips']==0) & (df_s_d_r['division_cd']!=0)]
df_divisions = df_divisions.rename(columns={'name':'division_name'})
df_divisions = df_divisions[['division_cd', 'division_name']]

#states
df_states = df_s_d_r[df_s_d_r['state_fips']!=0]
df_states = df_states.sort_values(by=['state_fips'])
df_states = df_states.rename(columns={'name':'state_name'})
df_states = df_states[['state_fips', 'region_cd', 'division_cd', 'state_name']]


#display(df_states)
#display(df_regions)
#display(df_divisions)


'''
NOTE: Not every county is a part of a CSA, CBSA, or MSA
'''

#CSA-CBSA-MSA
df_csa = pd.read_excel(os.path.join('data', 'list1_2020.xls'), header=2)
df_csa = df_csa.rename(columns={'FIPS State Code': 'state_fips', 'FIPS County Code': 'county_fips'})
df_csa = df_csa.dropna(subset=['county_fips'])
df_csa.county_fips = df_csa.county_fips.astype(int)
df_csa.state_fips = df_csa.state_fips.astype(int)


df_csa = df_csa.rename(columns={'CBSA Code': 'cbsa_cd',                                   'CBSA Title':'cbsa_name',                                   'CSA Code': 'csa_cd',                                   'CSA Title':'csa_name',                                   'Metropolitan/Micropolitan Statistical Area': 'cbsa_type',                                  })

df_csa = df_csa[['cbsa_cd', 'cbsa_name', 'csa_cd', 'csa_name', 'cbsa_type', 'state_fips', 'county_fips']]
df_csa = df_csa[(df_csa['state_fips']<= 56)]


#display(df_csa)


#joins

df_state_joined = pd.merge(df_states, df_regions, left_on='region_cd', right_on='region_cd', how='left')
df_state_joined = pd.merge(df_state_joined, df_divisions, left_on='division_cd', right_on='division_cd', how='left')

df_counties_final = pd.merge(df_counties, df_state_joined, left_on='state_fips', right_on='state_fips', how='left')

df_counties_final = pd.merge(df_counties_final, df_csa, left_on=['state_fips','county_fips'], right_on=['state_fips','county_fips'], how='left')

df_counties_final['county_fips'] = df_counties_final['county_fips'].apply(lambda x: '{0:0>3}'.format(x))
df_counties_final['state_fips'] = df_counties_final['state_fips'].apply(lambda x: '{0:0>2}'.format(x))

df_counties_final['combined_fips'] = df_counties_final["state_fips"] + df_counties_final["county_fips"]
df_counties_final['combined_name'] = df_counties_final["county_name"] + ', ' + df_counties_final["state_name"]



#display(df_counties_final)




# # Census ACS5

# In[4]:


api_key = ''
year='2018'
dsource='acs'
dname='acs5'
darea='profile'
cols=  'NAME,DP02_0001E,DP03_0005PE,DP03_0062E,DP03_0088E,DP03_0119PE,DP04_0002PE,DP04_0003PE,DP04_0046PE,DP04_0047PE,DP05_0001E,DP02_0066PE,DP02_0067PE,DP02_0065PE,DP03_0019PE,DP03_0020PE,DP03_0021PE,DP03_0022PE,DP03_0023PE,DP03_0024PE,DP03_0025E,DP05_0018E'
state='*'
county='*'

base_url = f'https://api.census.gov/data/{year}/{dsource}/{dname}/{darea}'

data_url = f'{base_url}?get={cols}&for=county:{county}&in=state:{state}&key={api_key}'
response=requests.get(data_url)

data=response.json()
df_acs=pd.DataFrame(data[1:], columns=data[0])
df_acs = df_acs.rename(columns={'DP02_0001E': 'total_HH',                                'DP03_0005PE': 'unemployment_perc',                                'DP03_0062E': 'median_hh_income',                                'DP03_0088E': 'per_capita_income',                                'DP03_0119PE': 'poverty_perc',                                'DP04_0002PE': 'housing_occupied_perc',                                'DP04_0003PE': 'housing_vacancy_perc',                                'DP04_0046PE': 'owner_perc',                                'DP04_0047PE': 'renter_perc',                                'DP05_0001E': 'tot_pop',                                'DP02_0066PE': 'edu_hs_and_higher_perc',                                'DP02_0067PE': 'edu_bachelors_and_higher_perc',                                'DP02_0065PE': 'edu_graduate_prof_perc',                                'DP03_0019PE': 'commute_mode_drove_alone',                                'DP03_0020PE': 'commute_mode_carpooled',                                'DP03_0021PE': 'commute_mode_public_transit',                                'DP03_0022PE': 'commute_mode_walked',                                'DP03_0023PE': 'commute_mode_other',                                'DP03_0024PE': 'commute_mode_wfh',                                'DP03_0025E': 'commute_time_in_min',                                'DP05_0018E': 'median_age',                                'state': 'state_fips',                                'county': 'county_fips',})


df_acs = df_acs.apply(pd.to_numeric, errors='ignore')


df_acs['county_fips'] = df_acs['county_fips'].apply(lambda x: '{0:0>3}'.format(x))
df_acs['state_fips'] = df_acs['state_fips'].apply(lambda x: '{0:0>2}'.format(x))





#calculate green commuting & ranks/percentiles
df_acs['commute_green_perc'] = (df_acs['commute_mode_carpooled'] + df_acs['commute_mode_public_transit'] + df_acs['commute_mode_walked'])                                     /                         (df_acs['commute_mode_drove_alone'] + df_acs['commute_mode_carpooled'] + df_acs['commute_mode_public_transit'] + df_acs['commute_mode_walked'])

df_acs['commute_green_rank'] = df_acs['commute_green_perc'].rank(method='min')
df_acs['commute_green_percentile'] = df_acs['commute_green_perc'].rank(pct=True)





#add ranks & percentiles
df_acs['unemployment_rank'] = df_acs['unemployment_perc'].rank(method='min')
df_acs['unemployment_percentile'] = df_acs['unemployment_perc'].rank(pct=True)

df_acs['median_hh_income_rank'] = df_acs['median_hh_income'].rank(method='min')
df_acs['median_hh_income_percentile'] = df_acs['median_hh_income'].rank(pct=True)

df_acs['per_capita_income_rank'] = df_acs['per_capita_income'].rank(method='min')
df_acs['per_capita_income_percentile'] = df_acs['per_capita_income'].rank(pct=True)

df_acs['poverty_rank'] = df_acs['poverty_perc'].rank(method='min')
df_acs['poverty_percentile'] = df_acs['poverty_perc'].rank(pct=True)

df_acs['tot_pop_rank'] = df_acs['tot_pop'].rank(method='min')
df_acs['tot_pop_percentile'] = df_acs['tot_pop'].rank(pct=True)

df_acs['edu_bachelors_and_higher_rank'] = df_acs['edu_bachelors_and_higher_perc'].rank(method='min')
df_acs['edu_bachelors_and_higher_percentile'] = df_acs['edu_bachelors_and_higher_perc'].rank(pct=True)

df_acs['median_age_rank'] = df_acs['median_age'].rank(method='min')
df_acs['median_age_percentile'] = df_acs['median_age'].rank(pct=True)

df_acs['commute_time_in_min_rank'] = df_acs['commute_time_in_min'].rank(method='min')
df_acs['commute_time_in_min_percentile'] = df_acs['commute_time_in_min'].rank(pct=True)

df_acs['housing_vacancy_rank'] = df_acs['housing_vacancy_perc'].rank(method='min')
df_acs['housing_vacancy_percentile'] = df_acs['housing_vacancy_perc'].rank(pct=True)

df_acs['housing_occupied_rank'] = df_acs['housing_occupied_perc'].rank(method='min')
df_acs['housing_occupied_percentile'] = df_acs['housing_occupied_perc'].rank(pct=True)

df_acs['owner_rank'] = df_acs['owner_perc'].rank(method='min')
df_acs['owner_percentile'] = df_acs['owner_perc'].rank(pct=True)

df_acs['renter_rank'] = df_acs['renter_perc'].rank(method='min')
df_acs['renter_percentile'] = df_acs['renter_perc'].rank(pct=True)


#display(df_acs)


# # Census Migration

# In[5]:
 
year='2018'
dsource='acs'
dname='flows'
cols='MOVEDIN,GEOID1,GEOID2,MOVEDOUT,FULL1_NAME,FULL2_NAME,MOVEDNET'
state='*'
county='*'

base_url = f'https://api.census.gov/data/{year}/{dsource}/{dname}'


data_url = f'{base_url}?get={cols}&for=county:{county}&in=state:{state}&key={api_key}'
response=requests.get(data_url)


data=response.json()
df_migration=pd.DataFrame(data[1:], columns=data[0])
df_migration = df_migration.rename(columns={'state':'state_fips', 'county':'county_fips'})

cols = ['MOVEDIN', 'MOVEDOUT', 'MOVEDNET']
df_migration[cols] = df_migration[cols].apply(pd.to_numeric, errors='ignore')

#exclude puerto rico ins AND outs, exclude non-counties, and exclude ins from other countries
df_migration = df_migration[~(df_migration.GEOID2.str.len() > 5)]
df_migration = df_migration[(df_migration['state_fips']!='72')]

df_migration['new_col'] = df_migration['GEOID2'].astype(str).str[0:2]
df_migration = df_migration[(df_migration['new_col']!='72')]
del df_migration['new_col']

df_migration = df_migration[df_migration['MOVEDNET'].notna()]



#display(df_migration)


###migration short
df_migration_short = df_migration.groupby(['state_fips', 'county_fips']).agg({'MOVEDIN': ['sum'], 'MOVEDOUT': ['sum'], 'MOVEDNET': ['sum']}).reset_index()
df_migration_short.columns = ["_".join(x) for x in df_migration_short.columns.ravel()]
df_migration_short = df_migration_short.rename(columns={'state_fips_':'state_fips', 'county_fips_':'county_fips', 'MOVEDNET_sum':'pop_net_mvmt_only_us', 'MOVEDIN_sum':'pop_in_mvmt_only_us', 'MOVEDOUT_sum':'pop_out_mvmt_only_us'})


#bring in pop
df_migration_short = pd.merge(df_migration_short, df_acs[['state_fips','county_fips', 'tot_pop']], left_on=['state_fips','county_fips'], right_on=['state_fips','county_fips'], how='left')
df_migration_short['pop_net_mvmt_only_us_percent_of_pop'] = df_migration_short['pop_net_mvmt_only_us']  / df_migration_short['tot_pop'] 
del df_migration_short['tot_pop'] 


#add ranks & percentiles
df_migration_short['pop_in_mvmt_only_us_rank'] = df_migration_short['pop_in_mvmt_only_us'].rank(method='min')
df_migration_short['pop_in_mvmt_only_us_percentile'] = df_migration_short['pop_in_mvmt_only_us'].rank(pct=True)

df_migration_short['pop_out_mvmt_only_us_rank'] = df_migration_short['pop_out_mvmt_only_us'].rank(method='min')
df_migration_short['pop_out_mvmt_only_us_percentile'] = df_migration_short['pop_out_mvmt_only_us'].rank(pct=True)

df_migration_short['pop_net_mvmt_only_us_rank'] = df_migration_short['pop_net_mvmt_only_us'].rank(method='min')
df_migration_short['pop_net_mvmt_only_us_percentile'] = df_migration_short['pop_net_mvmt_only_us'].rank(pct=True)

df_migration_short['pop_net_mvmt_only_us_percent_of_pop_rank'] = df_migration_short['pop_net_mvmt_only_us_percent_of_pop'].rank(method='min')
df_migration_short['pop_net_mvmt_only_us_percent_of_pop_percentile'] = df_migration_short['pop_net_mvmt_only_us_percent_of_pop'].rank(pct=True)



#display(df_migration_short)



# In[6]:


#check

#print(df_migration['MOVEDIN'].sum() - df_migration['MOVEDOUT'].sum())
#print(df_migration['MOVEDNET'].sum())


# In[7]:


'''
NOTE: this data has 2 records for each connection, with opposite data, see below code for an example
'''
#check
first = df_migration[(df_migration['GEOID1']=='01001') & (df_migration['GEOID2']=='01003') ]
second = df_migration[(df_migration['GEOID2']=='01001') & (df_migration['GEOID1']=='01003') ]

#display(first)
#display(second)


# # Census Urban/Rural

# In[14]:


df_ur = pd.read_excel(os.path.join('data', 'PctUrbanRural_County.xls'))
df_ur = df_ur.rename(columns={'STATE':'state_fips','COUNTY':'county_fips'})
df_ur = df_ur[['state_fips', 'county_fips', 'POPPCT_URBAN','POPPCT_RURAL','AREAPCT_URBAN','AREAPCT_RURAL','POPDEN_URBAN','POPDEN_RURAL']]
df_ur = df_ur[(df_ur['state_fips']<= 56)]


df_ur['county_fips'] = df_ur['county_fips'].apply(lambda x: '{0:0>3}'.format(x))
df_ur['state_fips'] = df_ur['state_fips'].apply(lambda x: '{0:0>2}'.format(x))


#add ranks & percentiles
df_ur['POPPCT_URBAN_rank'] = df_ur['POPPCT_URBAN'].rank(method='min')
df_ur['POPPCT_URBAN_percentile'] = df_ur['POPPCT_URBAN'].rank(pct=True)

df_ur['POPPCT_RURAL_rank'] = df_ur['POPPCT_RURAL'].rank(method='min')
df_ur['POPPCT_RURAL_percentile'] = df_ur['POPPCT_RURAL'].rank(pct=True)

df_ur['AREAPCT_URBAN_rank'] = df_ur['AREAPCT_URBAN'].rank(method='min')
df_ur['AREAPCT_URBAN_percentile'] = df_ur['AREAPCT_URBAN'].rank(pct=True)

df_ur['AREAPCT_RURAL_rank'] = df_ur['AREAPCT_RURAL'].rank(method='min')
df_ur['AREAPCT_RURAL_percentile'] = df_ur['AREAPCT_RURAL'].rank(pct=True)

df_ur['POPDEN_URBAN_rank'] = df_ur['POPDEN_URBAN'].rank(method='min')
df_ur['POPDEN_URBAN_percentile'] = df_ur['POPDEN_URBAN'].rank(pct=True)

df_ur['POPDEN_RURAL_rank'] = df_ur['POPDEN_RURAL'].rank(method='min')
df_ur['POPDEN_RURAL_percentile'] = df_ur['POPDEN_RURAL'].rank(pct=True)


df_ur['POPDEN_URBAN_percentile'] = df_ur['POPDEN_URBAN_percentile'].fillna(0)
df_ur['POPDEN_RURAL_percentile'] = df_ur['POPDEN_RURAL_percentile'].fillna(0)

df_ur['county_fips'] = np.where((df_ur['state_fips'] == '46') & (df_ur['county_fips'] == '113'), '102', df_ur['county_fips'])
df_ur['county_fips'] = np.where((df_ur['state_fips'] == '02') & (df_ur['county_fips'] == '270'), '158', df_ur['county_fips'])

#display(df_ur)


# # Presidential Elections (2000-2016)

# In[15]:


'''
NOTE: Alaska does not report out election results by county (Borough), but instead by House District. These change over
        the years are not a clean match to county. Therefore, we will need to use a state total for each 
        county and assume uniformity
'''

df_pres_elections = pd.read_csv(os.path.join('data', 'countypres_2000-2016.csv'))
df_pres_elections = df_pres_elections.dropna(subset=['FIPS'])
df_pres_elections.FIPS = df_pres_elections.FIPS.astype(int)
df_pres_elections.FIPS = df_pres_elections.FIPS.astype(str)

def FIPS_to_state_fips(c):
    if len(c['FIPS']) == 4:
        return c['FIPS'][:1]
    elif len(c['FIPS']) == 5:
        return c['FIPS'][:2]
    
def FIPS_to_county_fips(c):
    return c['FIPS'][-3:]
    


df_pres_elections['state_fips'] = df_pres_elections.apply(FIPS_to_state_fips, axis=1)
df_pres_elections['county_fips'] = df_pres_elections.apply(FIPS_to_county_fips, axis=1)

df_pres_elections['county_fips'] = df_pres_elections['county_fips'].apply(lambda x: '{0:0>3}'.format(x))
df_pres_elections['state_fips'] = df_pres_elections['state_fips'].apply(lambda x: '{0:0>2}'.format(x))



#limit cols
df_pres_elections = df_pres_elections[['year','state_fips', 'county_fips', 'candidate','party','candidatevotes','totalvotes']]

#categorize parties
def f(row):
    if row['party'] == 'democrat':
        val = 'democrat'
    elif row['party'] == 'republican':
        val = 'republican'
    else:
        val = 'other'
    return val

df_pres_elections['party'] = df_pres_elections.apply(f, axis=1)


#sum up by the new parties
df_pres_elections = df_pres_elections.groupby(by=['year','state_fips', 'county_fips','party']).agg({'candidatevotes': 'sum', 'totalvotes': 'max'}).reset_index()

#percent votes
df_pres_elections['percent_votes'] = df_pres_elections['candidatevotes'] / df_pres_elections['totalvotes']


#split alaska and non alaska
df_alaska = df_pres_elections[df_pres_elections['state_fips']=='02']
df_notalaska = df_pres_elections[df_pres_elections['state_fips']!='02']




#get state total for alaska for each year
df_alaska_grouped = df_alaska.groupby(by=['state_fips', 'year','party']).agg({'candidatevotes': 'sum'}).reset_index()
df_alaska_grouped['totalvotes'] = df_alaska_grouped.groupby(by=['year'], sort=False)['candidatevotes'].transform('sum')
df_alaska_grouped['percent_votes'] = df_alaska_grouped['candidatevotes'] / df_alaska_grouped['totalvotes']
df_alaska_grouped = df_alaska_grouped[['state_fips', 'year','party','percent_votes']]


#change alaska county_fips to match official fips
df_alaska_grouped['fips_lst'] = df_alaska_grouped.apply(lambda x: list(df_counties_final[df_counties_final['state_fips']=='02']['county_fips']), axis=1)
df_alaska_grouped = df_alaska_grouped.explode('fips_lst')
df_alaska_grouped = df_alaska_grouped.rename(columns={'fips_lst': 'county_fips'})
df_alaska = df_alaska_grouped



frames = [df_notalaska, df_alaska]

df_pres_elections = pd.concat(frames)


#drop total votes
del df_pres_elections['totalvotes']

#pivot data
df_pres_elections = df_pres_elections.pivot_table(index=["year", "state_fips", "county_fips"], 
                    columns='party', 
                    values=["candidatevotes", "percent_votes"]).reset_index()

df_pres_elections.columns = ['_'.join(col) for col in df_pres_elections.columns]
df_pres_elections = df_pres_elections.rename(columns={'year_':'year', 'state_fips_':'state_fips', 'county_fips_':'county_fips'})



df_pres_elections['latest_election_winner'] = np.where((df_pres_elections.percent_votes_democrat > df_pres_elections.percent_votes_republican) | (df_pres_elections.percent_votes_democrat > df_pres_elections.percent_votes_republican), "Democrat",   #when... then
                                     np.where((df_pres_elections.percent_votes_republican > df_pres_elections.percent_votes_democrat) | (df_pres_elections.percent_votes_republican > df_pres_elections.percent_votes_democrat), "Republican",
                                     np.where((df_pres_elections.percent_votes_other > df_pres_elections.percent_votes_democrat) | (df_pres_elections.percent_votes_other > df_pres_elections.percent_votes_republican), "Other",
                                     "Tie")))   

df_pres_elections['political_winning_margin'] = abs(df_pres_elections.percent_votes_democrat - df_pres_elections.percent_votes_republican)


df_pres_elections['political_scale'] = df_pres_elections.percent_votes_republican - df_pres_elections.percent_votes_democrat



df_pres_elections['political_lean'] = np.where((abs(df_pres_elections.percent_votes_democrat - df_pres_elections.percent_votes_republican) <= .02 ), "Toss-Up",   #when... then
                                     np.where((df_pres_elections.percent_votes_democrat - df_pres_elections.percent_votes_republican <= .1 ) & (df_pres_elections.percent_votes_democrat - df_pres_elections.percent_votes_republican > 0 ), "Lean Democrat",
                                     np.where((df_pres_elections.percent_votes_republican - df_pres_elections.percent_votes_democrat <= .1 ) & (df_pres_elections.percent_votes_republican - df_pres_elections.percent_votes_democrat > 0 ), "Lean Republican",
                                     np.where((df_pres_elections.percent_votes_democrat - df_pres_elections.percent_votes_republican > .1 ) & (df_pres_elections.percent_votes_democrat - df_pres_elections.percent_votes_republican > 0 ), "Solid Democrat",
                                     np.where((df_pres_elections.percent_votes_republican - df_pres_elections.percent_votes_democrat > .1 ) & (df_pres_elections.percent_votes_republican - df_pres_elections.percent_votes_democrat > 0 ), "Solid Republican",
                                     "Unknown")))))


#display(df_pres_elections)


# # Geog Area

# In[16]:


df_area = pd.read_csv(os.path.join('data', '2019_Gaz_counties_national.txt'), sep='\t')
df_area = df_area.rename(columns={'GEOID':'FIPS'})
df_area.FIPS = df_area.FIPS.astype(str)


def FIPS_to_state_fips(c):
    if len(c['FIPS']) == 4:
        return c['FIPS'][:1]
    elif len(c['FIPS']) == 5:
        return c['FIPS'][:2]
    
def FIPS_to_county_fips(c):
    return c['FIPS'][-3:]


df_area['state_fips'] = df_area.apply(FIPS_to_state_fips, axis=1)
df_area['county_fips'] = df_area.apply(FIPS_to_county_fips, axis=1)
df_area.state_fips = df_area.state_fips.astype(float)
df_area = df_area[(df_area['state_fips']<= 56)] #exclude PR

df_area = df_area.dropna(subset=['state_fips'])
df_area.state_fips = df_area.state_fips.astype(int)

#format as string
df_area['county_fips'] = df_area['county_fips'].apply(lambda x: '{0:0>3}'.format(x))
df_area['state_fips'] = df_area['state_fips'].apply(lambda x: '{0:0>2}'.format(x))


#add total_area
df_area['tot_area_sqmi'] = df_area['ALAND_SQMI'] + df_area['AWATER_SQMI']
df_area['tot_area_sqmi_rank'] = df_area['tot_area_sqmi'].rank(method='min')
df_area['tot_area_sqmi_percentile'] = df_area['tot_area_sqmi'].rank(pct=True)

#display(df_area)


# # Data Dictionary

# In[17]:


df_data_dict = pd.read_csv(os.path.join('data', 'Data Dictionary - external.csv'))


# #  Df to SQLite

# In[ ]:


import sqlite3


# In[ ]:


#open main connection
conn = sqlite3.connect(os.path.join('data', 'market_maven.sqlite'))


# In[ ]:


#write to db
df_counties_final.to_sql('county_ref', conn, if_exists='replace', index=False)
df_area.to_sql('area', conn, if_exists='replace', index=False)
df_pres_elections.to_sql('pres_elections', conn, if_exists='replace', index=False)
df_ur.to_sql('urban_rural', conn, if_exists='replace', index=False)
#df_migration.to_sql('migration', conn, if_exists='replace', index=False) #not used in prototype
df_migration_short.to_sql('migration_short', conn, if_exists='replace', index=False)
df_acs.to_sql('acs', conn, if_exists='replace', index=False)
df_data_dict.to_sql('data_dict', conn, if_exists='replace', index=False)


# # Add Weather & Similar Counties from Dan's DBs

# In[ ]:


from functools import reduce

#open connections
conn_dan_weather = sqlite3.connect(os.path.join('data', 'weather_data.sqlite'))
conn_dan_similar_counties = sqlite3.connect(os.path.join('data', 'similar_counties.sqlite'))

#read from dan weather db
df_avg_sunny_days = pd.read_sql_query("SELECT * FROM avg_sunny_days", conn_dan_weather)
df_avg_annual_temp = pd.read_sql_query("SELECT * FROM avg_annual_temp", conn_dan_weather)
df_avg_fall_temp = pd.read_sql_query("SELECT * FROM avg_fall_temp", conn_dan_weather)
df_avg_winter_temp = pd.read_sql_query("SELECT * FROM avg_winter_temp", conn_dan_weather)
df_avg_spring_temp = pd.read_sql_query("SELECT * FROM avg_spring_temp", conn_dan_weather)
df_avg_summer_temp = pd.read_sql_query("SELECT * FROM avg_summer_temp", conn_dan_weather)

#read from dan similar counties db
df_similar_counties = pd.read_sql_query("SELECT * FROM similar_counties", conn_dan_similar_counties)


#combine weather tables into 1 table
data_frames = [df_avg_sunny_days, df_avg_annual_temp, df_avg_fall_temp, df_avg_winter_temp, df_avg_spring_temp, df_avg_summer_temp]
df_weather = reduce(lambda  left,right: pd.merge(left,right,on=['state_fips'],how='outer'), data_frames)



#write to main db
df_weather.to_sql('weather', conn, if_exists='replace', index=False)
df_similar_counties.to_sql('similar_counties', conn, if_exists='replace', index=False)


# # Create Views

# In[ ]:


c = conn.cursor()

c.execute('''
DROP VIEW IF EXISTS metrics_v
  ''')


c.execute('''
CREATE VIEW metrics_v AS 
    SELECT  A.state_fips, 
            A.county_fips,
            A.combined_fips,
            A.state_name,
            A.county_name,
            A.combined_name,
            A.CSA_name as csa_name,
            A.division_name,
            A.region_name,
            B.tot_pop,
            B.total_HH as total_hh,
            B.unemployment_perc,
            B.median_hh_income,
            B.per_capita_income,
            B.poverty_perc,
            B.housing_occupied_perc,
            B.housing_vacancy_perc,
            B.owner_perc,
            B.renter_perc,
            B.edu_bachelors_and_higher_perc,
            B.commute_green_perc,
            B.commute_time_in_min,
            B.median_age,
            C.POPPCT_URBAN as poppct_urban,
            C.POPPCT_RURAL as poppct_rural,
            C.AREAPCT_URBAN as areapct_urban,
            C.AREAPCT_RURAL as areapct_rural,
            C.POPDEN_URBAN as popden_urban,
            C.POPDEN_RURAL as popden_rural,
            D.tot_area_sqmi,
            E.political_lean,
            E.political_scale,
            F.avg_sunny_days,
            F.avg_annual_temp,
            F.avg_fall_temp,
            F.avg_winter_temp,
            F.avg_spring_temp,
            F.avg_summer_temp,
            H.pop_in_mvmt_only_us,
            H.pop_out_mvmt_only_us,
            H.pop_net_mvmt_only_us,
            H.pop_net_mvmt_only_us_percent_of_pop,

            B.per_capita_income_percentile,
            B.tot_pop_percentile,
            B.median_hh_income_percentile,
            B.poverty_percentile,
            B.median_age_percentile,
            B.commute_time_in_min_percentile,
            B.edu_bachelors_and_higher_percentile,
            B.unemployment_percentile,
            B.commute_green_percentile,
            B.housing_vacancy_percentile,
            B.housing_occupied_percentile,
            B.owner_percentile,
            B.renter_percentile,
            C.POPPCT_URBAN_percentile as poppct_urban_percentile,
            C.POPPCT_RURAL_percentile as poppct_rural_percentile,
            C.AREAPCT_URBAN_percentile as areapct_urban_percentile,
            C.AREAPCT_RURAL_percentile as areapct_rural_percentile,
            C.POPDEN_URBAN_percentile as popden_urban_percentile,
            C.POPDEN_RURAL_percentile as popden_rural_percentile,
            D.tot_area_sqmi_percentile,
            F.avg_sunny_days_percentile,
            F.avg_annual_temp_percentile,
            F.avg_fall_temp_percentile,
            F.avg_winter_temp_percentile,
            F.avg_spring_temp_percentile,
            F.avg_summer_temp_percentile,
            H.pop_in_mvmt_only_us_percentile,
            H.pop_out_mvmt_only_us_percentile,
            H.pop_net_mvmt_only_us_percentile,
            H.pop_net_mvmt_only_us_percent_of_pop_percentile
   
            
    FROM county_ref A
    LEFT JOIN acs B ON A.state_fips = B.state_fips AND A.county_fips = B.county_fips
    LEFT JOIN urban_rural C ON A.state_fips = C.state_fips AND A.county_fips = C.county_fips
    LEFT JOIN area D ON A.state_fips = D.state_fips AND A.county_fips = D.county_fips
    LEFT JOIN (select * from pres_elections where year = 2016) E ON A.state_fips = E.state_fips AND A.county_fips = E.county_fips
    LEFT JOIN weather F ON A.state_fips = F.state_fips
    LEFT JOIN migration_short H ON A.state_fips = H.state_fips AND A.county_fips = H.county_fips
  ''')




c.execute('''
DROP VIEW IF EXISTS metrics_no_percentiles_v
  ''')


c.execute('''
CREATE VIEW metrics_no_percentiles_v AS 
    SELECT  A.state_fips, 
            A.county_fips,
            A.combined_fips,
            A.state_name,
            A.county_name,
            A.combined_name,
            A.CSA_name as csa_name,
            A.division_name,
            A.region_name,
            B.tot_pop,
            B.total_HH as total_hh,
            B.unemployment_perc,
            B.median_hh_income,
            B.per_capita_income,
            B.poverty_perc,
            B.housing_occupied_perc,
            B.housing_vacancy_perc,
            B.owner_perc,
            B.renter_perc,
            B.edu_bachelors_and_higher_perc,
            B.commute_green_perc,
            B.commute_time_in_min,
            B.median_age,
            C.POPPCT_URBAN as poppct_urban,
            C.POPPCT_RURAL as poppct_rural,
            C.AREAPCT_URBAN as areapct_urban,
            C.AREAPCT_RURAL as areapct_rural,
            C.POPDEN_URBAN as popden_urban,
            C.POPDEN_RURAL as popden_rural,
            D.tot_area_sqmi,
            E.political_lean,
            E.political_scale,
            F.avg_sunny_days,
            F.avg_annual_temp,
            F.avg_fall_temp,
            F.avg_winter_temp,
            F.avg_spring_temp,
            F.avg_summer_temp,
            H.pop_in_mvmt_only_us,
            H.pop_out_mvmt_only_us,
            H.pop_net_mvmt_only_us,
            H.pop_net_mvmt_only_us_percent_of_pop
   
            
    FROM county_ref A
    LEFT JOIN acs B ON A.state_fips = B.state_fips AND A.county_fips = B.county_fips
    LEFT JOIN urban_rural C ON A.state_fips = C.state_fips AND A.county_fips = C.county_fips
    LEFT JOIN area D ON A.state_fips = D.state_fips AND A.county_fips = D.county_fips
    LEFT JOIN (select * from pres_elections where year = 2016) E ON A.state_fips = E.state_fips AND A.county_fips = E.county_fips
    LEFT JOIN weather F ON A.state_fips = F.state_fips
    LEFT JOIN migration_short H ON A.state_fips = H.state_fips AND A.county_fips = H.county_fips
  ''')





c.execute('''
DROP VIEW IF EXISTS similar_counties_v
  ''')


c.execute('''
CREATE VIEW similar_counties_v AS 
    SELECT  A.combined_fips, 
            B.state_name,
            B.county_name,
            B.combined_name,
            A.similar_combined_fips,
            C.combined_name as similar_combined_name,
            A.rank


    FROM similar_counties A
    LEFT JOIN county_ref B ON A.combined_fips = B.combined_fips
    LEFT JOIN county_ref C ON A.similar_combined_fips = C.combined_fips
  ''')


# # Close Conections

# In[ ]:


conn.close()
conn_dan_similar_counties.close()
conn_dan_weather.close()

