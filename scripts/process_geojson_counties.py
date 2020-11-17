import json
import os

import pandas as pd

properties = [
    # ECONOMY
    'median_hh_income',
    'per_capita_income',
    'unemployment_perc',
    'poverty_perc',
    # SOCIAL
    'median_age',
    'edu_bachelors_and_higher_perc',
    'commute_green_perc',
    'commute_time_in_min',
    'political_scale',
    # WEATHER
    'avg_sunny_days',
    'avg_annual_temp',
    'avg_fall_temp',
    'avg_winter_temp',
    'avg_spring_temp',
    'avg_summer_temp',
    # POPULATION
    'tot_pop',
    'pop_in_mvmt_only_us',
    'pop_out_mvmt_only_us',
    'pop_net_mvmt_only_us',
    'pop_net_mvmt_only_us_percent_of_pop',
    # URBAN/RURAL
    'tot_area_sqmi',
    'poppct_urban',
    'poppct_rural',
    'areapct_urban',
    'areapct_rural',
    'popden_urban',
    'popden_rural',
    # REAL ESTATE
    'housing_occupied_perc',
    'housing_vacancy_perc',
    'owner_perc',
    'renter_perc'
]

metrics_v_df = pd.read_csv('metrics_v.csv')
metrics_v_df['combined_fips'] = metrics_v_df['combined_fips'].astype('int')

# if 'green_commuting_perc' not in metrics_v_df:
#     try:
#         metrics_v_df['green_commuting_perc'] = (metrics_v_df['commute_mode_carpooled'] + metrics_v_df['commute_mode_walked'] + metrics_v_df['commute_mode_public_transit']) / (metrics_v_df['commute_mode_carpooled'] + metrics_v_df['commute_mode_walked'] + metrics_v_df['commute_mode_public_transit'] + metrics_v_df['commute_mode_drove_alone'])
#     except:
#         metrics_v_df['green_commuting_perc'] = 0

# if 'total_area' not in metrics_v_df:
#     try:
#         metrics_v_df['total_area'] = metrics_v_df['ALAND_SQMI'] + metrics_v_df['AWATER_SQMI']
#     except:
#         metrics_v_df['total_area'] = 0

with open('geojson-counties.json') as json_file:
    geodict = json.load(json_file)

geodict_features = geodict['features']

features = []

for index, feature in enumerate(geodict_features):
    state = feature['properties']['STATE']
    county = feature['properties']['COUNTY']
    combined_fips = int(state + county)
    for property in properties:
        try:
            property_value = metrics_v_df[metrics_v_df['combined_fips'] == combined_fips][property].values[0]
            property_value = str(property_value)
        except:
            property_value = str(0)
        feature['properties'][property.upper()] = property_value
    features.append(feature)

geodict['features'] = features

with open('geojson-counties-fips-updated.json', 'w') as json_file:
    json.dump(geodict, json_file)