# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app import app


#data
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(ROOT_DIR, 'assets', 'market_maven.sqlite'))
df_metrics = pd.read_sql_query(''' select * from metrics_v''', conn)
df_similar_counties = pd.read_sql_query(''' select * from similar_counties_v''', conn)
conn.close()


#dict of dropdown options; key = state, values = counties
dropdowns_list_dict_names = df_metrics.groupby('state_name')['county_name'].apply(lambda x: x.unique().tolist()).to_dict()
#dropdowns_list_dict_fips = df_metrics.groupby('state_fips')['county_fips'].apply(lambda x: x.unique().tolist()).to_dict()
    
#county selected
@app.callback(
    Output('county_dropdown', 'options'),
    [Input('state_dropdown', 'value')])
def set_county_options(selected_state):
    if selected_state is not None:
        return [{'label': i, 'value': i} for i in dropdowns_list_dict_names[selected_state]]
    else:
        raise PreventUpdate


def fips_to_name(fips):
        county_name = df_metrics[df_metrics['combined_fips'] == str(fips)]['county_name'].values[0]
        state_name = df_metrics[df_metrics['combined_fips'] == str(fips)]['state_name'].values[0]
        return county_name, state_name

def name_to_fips(county_name, state_name):
        fips = df_metrics[(df_metrics['county_name'] == county_name) & (df_metrics['state_name'] == state_name)]['combined_fips'].values[0]
        return fips


def get_metric(metric=None, selected_state='New Jersey', selected_county='Mercer County'):
        metric_value = None

        if metric.split('_')[0] == 'similar':
                df_metrics_filtered = df_similar_counties[(df_similar_counties['state_name']==selected_state) & (df_similar_counties['county_name']==selected_county)].sort_values(['rank']).reset_index()
        else:
                df_metrics_filtered = df_metrics[(df_metrics['state_name']==selected_state) & (df_metrics['county_name']==selected_county)]
                metric_value = df_metrics_filtered.iloc[0][metric]

        if metric == 'combined_name':
                return metric_value
        elif metric == 'unemployment_perc':
                return "{0:.1f}%".format(metric_value)
        elif metric == 'median_hh_income':
                return '${:,.0f}'.format(metric_value)
        elif metric == 'per_capita_income':
                return '${:,.0f}'.format(metric_value)
        elif metric == 'poverty_perc':
                return "{0:.1f}%".format(metric_value)
        elif metric == 'median_age':
                return metric_value
        elif metric == 'political_lean':
                return metric_value
        elif metric == 'commute_time_in_min':
                return str(int(metric_value)) + " min"
        elif metric == 'edu_bachelors_and_high_per':
                return  "{0:.1f}%".format(metric_value)
        elif metric == 'avg_sunny_days':
                return metric_value
        elif metric == 'avg_annual_temp':
                return str(int(metric_value)) + " degrees"
        elif metric == 'unemployment_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'median_hh_income_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'poverty_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'per_capita_income_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'median_age_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'edu_bachelors_and_higher_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'commute_time_in_min_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'tot_pop':
                return '{:,}'.format(metric_value)
        elif metric == 'tot_pop_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'commute_green_perc':
                return "{0:.1f}%".format(metric_value*100)
        elif metric == 'commute_green_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_sunny_days_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_annual_temp_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_winter_temp_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_summer_temp_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_winter_temp':
                return str(int(metric_value)) + " degrees"
        elif metric == 'avg_summer_temp':
                return str(int(metric_value)) + " degrees"
        elif metric == 'avg_fall_temp_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_spring_temp_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'avg_fall_temp':
                return str(int(metric_value)) + " degrees"
        elif metric == 'avg_spring_temp':
                return str(int(metric_value)) + " degrees"
        elif metric == 'pop_in_mvmt_only_us':
                return '{:,.0f}'.format(metric_value)
        elif metric == 'pop_in_mvmt_only_us_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'pop_out_mvmt_only_us':
                return '{:,.0f}'.format(metric_value)
        elif metric == 'pop_out_mvmt_only_us_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'pop_net_mvmt_only_us':
                return '{:,.0f}'.format(metric_value)
        elif metric == 'pop_net_mvmt_only_us_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'pop_net_mvmt_only_us_percent_of_pop':
                return "{0:.1f}%".format(metric_value*100)
        elif metric == 'pop_net_mvmt_only_us_percent_of_pop_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'poppct_urban':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'poppct_rural':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'areapct_urban':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'areapct_rural':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'poppct_urban_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'poppct_rural_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'areapct_urban_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'areapct_rural_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'popden_urban':
                return '{0:,.2f}'.format(metric_value)
        elif metric == 'popden_rural':
                return '{0:,.2f}'.format(metric_value)
        elif metric == 'popden_urban_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'popden_rural_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'tot_area_sqmi':
                return '{0:,.2f}'.format(metric_value)
        elif metric == 'tot_area_sqmi_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'combined_fips':
                return str(metric_value)
        elif metric == 'county_name':
                return metric_value
        elif metric == 'state_name':
                return metric_value
        elif metric == 'csa_name':
                return metric_value
        elif metric == 'division_name':
                return metric_value
        elif metric == 'region_name':
                return metric_value
        elif metric == 'housing_occupied_perc':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'housing_occupied_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'housing_vacancy_perc':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'housing_vacancy_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'owner_perc':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'owner_percentile':
                return str(ord(int(metric_value*100))) + " pctl"
        elif metric == 'renter_perc':
                return "{0:.2f}%".format(metric_value)
        elif metric == 'renter_percentile':
                return str(ord(int(metric_value*100))) + " pctl" 
        elif metric.split('_')[0] == 'similar':
                index = int(metric.split('_')[3])
                metric_value = df_metrics_filtered.iloc[index]['similar_combined_name']
                county_name = metric_value.split(',')[0].strip()
                state_name = metric_value.split(',')[1].strip()
                fips = name_to_fips(county_name=county_name, state_name=state_name)
                return dcc.Link(children=metric_value, href=f'/details?fips={fips}')

        return metric_value


@app.callback(
    [Output('name_sel', 'children'),
     Output('unemp_rt', 'children'),
     Output('median_hh_inc', 'children'),
     Output('per_cap_inc', 'children'),
     Output('poverty', 'children'),
     Output('age', 'children'),
     Output('political_lean', 'children'),
     Output('commute_time_in_min', 'children'),
     Output('unemployment_percentile', 'children'),
     Output('bach_and_higher', 'children'),
     Output('avg_sunny_days', 'children'),
     Output('avg_annual_temp', 'children'),
     Output('median_hh_income_percentile', 'children'),
     Output('poverty_percentile', 'children'),
     Output('per_capita_income_percentile', 'children'),
     Output('median_age_percentile', 'children'),
     Output('edu_bachelors_and_higher_percentile', 'children'),
     Output('commute_time_in_min_percentile', 'children'),
     Output('tot_pop', 'children'),
     Output('tot_pop_percentile', 'children'),
     Output('commute_green', 'children'),
     Output('commute_green_percentile', 'children'),
     Output('avg_sunny_days_percentile', 'children'),
     Output('avg_annual_temp_percentile', 'children'),
     Output('avg_winter_temp_percentile', 'children'),
     Output('avg_summer_temp_percentile', 'children'),
     Output('avg_winter_temp', 'children'),
     Output('avg_summer_temp', 'children'),
     
     Output('avg_fall_temp_percentile', 'children'),
     Output('avg_spring_temp_percentile', 'children'),
     Output('avg_fall_temp', 'children'),
     Output('avg_spring_temp', 'children'),
     
     Output('pop_in_mvmt_only_us', 'children'),
     Output('pop_in_mvmt_only_us_percentile', 'children'),
     Output('pop_out_mvmt_only_us', 'children'),
     Output('pop_out_mvmt_only_us_percentile', 'children'),
     Output('pop_net_mvmt_only_us', 'children'),
     Output('pop_net_mvmt_only_us_percentile', 'children'),
     Output('pop_net_mvmt_only_us_percent_of_pop', 'children'),
     Output('pop_net_mvmt_only_us_percent_of_pop_percentile', 'children'),
     
     Output('poppct_urban', 'children'),
     Output('poppct_rural', 'children'),
     Output('areapct_urban', 'children'),
     Output('areapct_rural', 'children'),
     Output('poppct_urban_percentile', 'children'),
     Output('poppct_rural_percentile', 'children'),
     Output('areapct_urban_percentile', 'children'),
     Output('areapct_rural_percentile', 'children'),
     Output('popden_urban', 'children'),
     Output('popden_rural', 'children'),
     Output('popden_urban_percentile', 'children'),
     Output('popden_rural_percentile', 'children'),
     
     
     
     
     Output('tot_area_sqmi', 'children'),
     Output('tot_area_sqmi_percentile', 'children'),
     
     Output('combined_fips', 'children'),
     Output('county_name', 'children'),
     Output('state_name', 'children'),
     Output('csa_name', 'children'),
     Output('division_name', 'children'),
     Output('region_name', 'children'),
     
     Output('similar_counties_0', 'children'),
     Output('similar_counties_1', 'children'),
     Output('similar_counties_2', 'children'),
     Output('similar_counties_3', 'children'),
     Output('similar_counties_4', 'children'),
     
     Output('housing_occupied_perc', 'children'),
     Output('housing_occupied_percentile', 'children'),
     Output('housing_vacancy_perc', 'children'),
     Output('housing_vacancy_percentile', 'children'),
     Output('owner_perc', 'children'),
     Output('owner_percentile', 'children'),
     Output('renter_perc', 'children'),
     Output('renter_percentile', 'children')     
     
     
          ],
    [Input('state_dropdown', 'value'),
     Input('county_dropdown', 'value')])
def callback_a(selected_state, selected_county):
    if selected_state is not None and selected_county is not None and selected_state in dropdowns_list_dict_names and selected_county in dropdowns_list_dict_names[selected_state]:

        df_metrics_filtered = df_metrics[(df_metrics['state_name']==selected_state) & (df_metrics['county_name']==selected_county)]
        df_similar_counties_filtered = df_similar_counties[(df_similar_counties['state_name']==selected_state) & (df_similar_counties['county_name']==selected_county)].sort_values(['rank']).reset_index()
        
        name = df_metrics_filtered.iloc[0]['combined_name']
        unemp = df_metrics_filtered.iloc[0]['unemployment_perc']
        inc_HH = df_metrics_filtered.iloc[0]['median_hh_income']
        inc_capita = df_metrics_filtered.iloc[0]['per_capita_income']
        poverty = df_metrics_filtered.iloc[0]['poverty_perc']
        age = df_metrics_filtered.iloc[0]['median_age']
        political_lean = df_metrics_filtered.iloc[0]['political_lean']
        commute_time_in_min = df_metrics_filtered.iloc[0]['commute_time_in_min']
        bach_and_higher = df_metrics_filtered.iloc[0]['edu_bachelors_and_higher_perc']
        avg_sunny_days = df_metrics_filtered.iloc[0]['avg_sunny_days']
        avg_annual_temp = df_metrics_filtered.iloc[0]['avg_annual_temp']
        unemployment_percentile = df_metrics_filtered.iloc[0]['unemployment_percentile']
        median_hh_income_percentile = df_metrics_filtered.iloc[0]['median_hh_income_percentile']
        poverty_percentile = df_metrics_filtered.iloc[0]['poverty_percentile']
        per_capita_income_percentile = df_metrics_filtered.iloc[0]['per_capita_income_percentile']
        median_age_percentile = df_metrics_filtered.iloc[0]['median_age_percentile']
        edu_bachelors_and_higher_percentile = df_metrics_filtered.iloc[0]['edu_bachelors_and_higher_percentile']
        commute_time_in_min_percentile = df_metrics_filtered.iloc[0]['commute_time_in_min_percentile']
        tot_pop = df_metrics_filtered.iloc[0]['tot_pop']
        tot_pop_percentile = df_metrics_filtered.iloc[0]['tot_pop_percentile']
        commute_green_perc = df_metrics_filtered.iloc[0]['commute_green_perc']
        commute_green_percentile = df_metrics_filtered.iloc[0]['commute_green_percentile']
        avg_sunny_days_percentile = df_metrics_filtered.iloc[0]['avg_sunny_days_percentile']
        avg_annual_temp_percentile = df_metrics_filtered.iloc[0]['avg_annual_temp_percentile']
        avg_winter_temp_percentile = df_metrics_filtered.iloc[0]['avg_winter_temp_percentile']
        avg_summer_temp_percentile = df_metrics_filtered.iloc[0]['avg_summer_temp_percentile']
        avg_winter_temp = df_metrics_filtered.iloc[0]['avg_winter_temp']
        avg_summer_temp = df_metrics_filtered.iloc[0]['avg_summer_temp']
        
        avg_fall_temp_percentile = df_metrics_filtered.iloc[0]['avg_fall_temp_percentile']
        avg_spring_temp_percentile = df_metrics_filtered.iloc[0]['avg_spring_temp_percentile']
        avg_fall_temp = df_metrics_filtered.iloc[0]['avg_fall_temp']
        avg_spring_temp = df_metrics_filtered.iloc[0]['avg_spring_temp']
        
        pop_in_mvmt_only_us = df_metrics_filtered.iloc[0]['pop_in_mvmt_only_us']
        pop_in_mvmt_only_us_percentile = df_metrics_filtered.iloc[0]['pop_in_mvmt_only_us_percentile']
        pop_out_mvmt_only_us = df_metrics_filtered.iloc[0]['pop_out_mvmt_only_us']
        pop_out_mvmt_only_us_percentile = df_metrics_filtered.iloc[0]['pop_out_mvmt_only_us_percentile']
        pop_net_mvmt_only_us = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us']
        pop_net_mvmt_only_us_percentile = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us_percentile']
        pop_net_mvmt_only_us_percent_of_pop = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us_percent_of_pop']
        pop_net_mvmt_only_us_percent_of_pop_percentile = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us_percent_of_pop_percentile']
    
        poppct_urban = df_metrics_filtered.iloc[0]['poppct_urban']
        poppct_rural = df_metrics_filtered.iloc[0]['poppct_rural']
        areapct_urban = df_metrics_filtered.iloc[0]['areapct_urban']
        areapct_rural = df_metrics_filtered.iloc[0]['areapct_rural']
        poppct_urban_percentile = df_metrics_filtered.iloc[0]['poppct_urban_percentile']
        poppct_rural_percentile = df_metrics_filtered.iloc[0]['poppct_rural_percentile']
        areapct_urban_percentile = df_metrics_filtered.iloc[0]['areapct_urban_percentile']
        areapct_rural_percentile = df_metrics_filtered.iloc[0]['areapct_rural_percentile']
        popden_urban = df_metrics_filtered.iloc[0]['popden_urban']
        popden_rural = df_metrics_filtered.iloc[0]['popden_rural']
        
        popden_urban_percentile = df_metrics_filtered.iloc[0]['popden_urban_percentile']
        popden_rural_percentile = df_metrics_filtered.iloc[0]['popden_rural_percentile']
    
        tot_area_sqmi = df_metrics_filtered.iloc[0]['tot_area_sqmi']
        tot_area_sqmi_percentile = df_metrics_filtered.iloc[0]['tot_area_sqmi_percentile']
        
        combined_fips = df_metrics_filtered.iloc[0]['combined_fips']
        county_name = df_metrics_filtered.iloc[0]['county_name']
        state_name = df_metrics_filtered.iloc[0]['state_name']
        csa_name = df_metrics_filtered.iloc[0]['csa_name']
        division_name = df_metrics_filtered.iloc[0]['division_name']
        region_name = df_metrics_filtered.iloc[0]['region_name']
    
        fips = name_to_fips(county_name=selected_county, state_name=selected_state)
        similar_counties_0 = dcc.Link(children=df_similar_counties_filtered.iloc[0]['similar_combined_name'], href=f'/details?fips={fips}')
        similar_counties_1 = dcc.Link(children=df_similar_counties_filtered.iloc[1]['similar_combined_name'], href=f'/details?fips={fips}')
        similar_counties_2 = dcc.Link(children=df_similar_counties_filtered.iloc[2]['similar_combined_name'], href=f'/details?fips={fips}')
        similar_counties_3 = dcc.Link(children=df_similar_counties_filtered.iloc[3]['similar_combined_name'], href=f'/details?fips={fips}')
        similar_counties_4 = dcc.Link(children=df_similar_counties_filtered.iloc[4]['similar_combined_name'], href=f'/details?fips={fips}')

        # similar_counties_0 = df_similar_counties_filtered.iloc[0]['similar_combined_name']
        # similar_counties_1 = df_similar_counties_filtered.iloc[1]['similar_combined_name']
        # similar_counties_2 = df_similar_counties_filtered.iloc[2]['similar_combined_name']
        # similar_counties_3 = df_similar_counties_filtered.iloc[3]['similar_combined_name']
        # similar_counties_4 = df_similar_counties_filtered.iloc[4]['similar_combined_name']
    
        housing_occupied_perc = df_metrics_filtered.iloc[0]['housing_occupied_perc']
        housing_occupied_percentile = df_metrics_filtered.iloc[0]['housing_occupied_percentile']
        housing_vacancy_perc = df_metrics_filtered.iloc[0]['housing_vacancy_perc']
        housing_vacancy_percentile = df_metrics_filtered.iloc[0]['housing_vacancy_percentile']
        owner_perc = df_metrics_filtered.iloc[0]['owner_perc']
        owner_percentile = df_metrics_filtered.iloc[0]['owner_percentile']
        renter_perc = df_metrics_filtered.iloc[0]['renter_perc']
        renter_percentile = df_metrics_filtered.iloc[0]['renter_percentile']    
  
    
    
        return name, \
                "{0:.1f}%".format(unemp), \
                '${:,.0f}'.format(inc_HH), \
                '${:,.0f}'.format(inc_capita), \
                "{0:.1f}%".format(poverty), \
                age, \
                political_lean, \
                str(int(commute_time_in_min)) + " min", \
                str(ord(int(unemployment_percentile*100))) + " pctl", \
                "{0:.1f}%".format(bach_and_higher), \
                avg_sunny_days, \
                str(int(avg_annual_temp)) + " degrees", \
                str(ord(int(median_hh_income_percentile*100))) + " pctl", \
                str(ord(int(poverty_percentile*100))) + " pctl", \
                str(ord(int(per_capita_income_percentile*100))) + " pctl", \
                str(ord(int(median_age_percentile*100))) + " pctl", \
                str(ord(int(edu_bachelors_and_higher_percentile*100))) + " pctl", \
                str(ord(int(commute_time_in_min_percentile*100))) + " pctl", \
                '{:,}'.format(tot_pop), \
                str(ord(int(tot_pop_percentile*100))) + " pctl", \
                "{0:.1f}%".format(commute_green_perc*100), \
                str(ord(int(commute_green_percentile*100))) + " pctl", \
                str(ord(int(avg_sunny_days_percentile*100))) + " pctl", \
                str(ord(int(avg_annual_temp_percentile*100))) + " pctl", \
                str(ord(int(avg_winter_temp_percentile*100))) + " pctl", \
                str(ord(int(avg_summer_temp_percentile*100))) + " pctl", \
                str(int(avg_winter_temp)) + " degrees", \
                str(int(avg_summer_temp)) + " degrees", \
                str(ord(int(avg_fall_temp_percentile*100))) + " pctl", \
                str(ord(int(avg_spring_temp_percentile*100))) + " pctl", \
                str(int(avg_fall_temp)) + " degrees", \
                str(int(avg_spring_temp)) + " degrees", \
                '{:,.0f}'.format(pop_in_mvmt_only_us), \
                str(ord(int(pop_in_mvmt_only_us_percentile*100))) + " pctl", \
                '{:,.0f}'.format(pop_out_mvmt_only_us), \
                str(ord(int(pop_out_mvmt_only_us_percentile*100))) + " pctl", \
                '{:,.0f}'.format(pop_net_mvmt_only_us), \
                str(ord(int(pop_net_mvmt_only_us_percentile*100))) + " pctl", \
                "{0:.1f}%".format(pop_net_mvmt_only_us_percent_of_pop*100), \
                str(ord(int(pop_net_mvmt_only_us_percent_of_pop_percentile*100))) + " pctl", \
                "{0:.2f}%".format(poppct_urban), \
                "{0:.2f}%".format(poppct_rural), \
                "{0:.2f}%".format(areapct_urban), \
                "{0:.2f}%".format(areapct_rural), \
                str(ord(int(poppct_urban_percentile*100))) + " pctl", \
                str(ord(int(poppct_rural_percentile*100))) + " pctl", \
                str(ord(int(areapct_urban_percentile*100))) + " pctl", \
                str(ord(int(areapct_rural_percentile*100))) + " pctl", \
                '{0:,.2f}'.format(popden_urban), \
                '{0:,.2f}'.format(popden_rural), \
                str(ord(int(popden_urban_percentile*100))) + " pctl", \
                str(ord(int(popden_rural_percentile*100))) + " pctl", \
                '{0:,.2f}'.format(tot_area_sqmi), \
                str(ord(int(tot_area_sqmi_percentile*100))) + " pctl", \
                str(combined_fips), \
                county_name, \
                state_name, \
                csa_name, \
                division_name, \
                region_name, \
                similar_counties_0, \
                similar_counties_1, \
                similar_counties_2, \
                similar_counties_3, \
                similar_counties_4, \
                "{0:.2f}%".format(housing_occupied_perc), \
                str(ord(int(housing_occupied_percentile*100))) + " pctl", \
                "{0:.2f}%".format(housing_vacancy_perc), \
                str(ord(int(housing_vacancy_percentile*100))) + " pctl", \
                "{0:.2f}%".format(owner_perc), \
                str(ord(int(owner_percentile*100))) + " pctl", \
                "{0:.2f}%".format(renter_perc), \
                str(ord(int(renter_percentile*100))) + " pctl"           
                
                
    else:
            return [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]


    
            
            
            
            
            
#comparison selected
@app.callback(
    Output('county_dropdown_comparison', 'options'),
    [Input('state_dropdown_comparison', 'value')])
def set_county_options_comparison(selected_state):
    if selected_state is not None:
        return [{'label': i, 'value': i} for i in dropdowns_list_dict_names[selected_state]]
    else:
        raise PreventUpdate




@app.callback(
    [Output('name_sel_comparison', 'children'),
     Output('vs_comparison', 'children'),
     Output('unemp_rt_comparison', 'children'),
     Output('median_hh_inc_comparison', 'children'),
     Output('per_cap_inc_comparison', 'children'),
     Output('poverty_comparison', 'children'),
     Output('age_comparison', 'children'),
     Output('political_lean_comparison', 'children'),
     Output('commute_time_in_min_comparison', 'children'),
     Output('unemployment_percentile_comparison', 'children'),
     Output('bach_and_higher_comparison', 'children'),
     Output('avg_sunny_days_comparison', 'children'),
     Output('avg_annual_temp_comparison', 'children'),
     Output('median_hh_income_percentile_comparison', 'children'),
     Output('poverty_percentile_comparison', 'children'),
     Output('per_capita_income_percentile_comparison', 'children'),
     Output('median_age_percentile_comparison', 'children'),
     Output('edu_bachelors_and_higher_percentile_comparison', 'children'),
     Output('commute_time_in_min_percentile_comparison', 'children'),
     Output('tot_pop_comparison', 'children'),
     Output('tot_pop_percentile_comparison', 'children'),
     Output('commute_green_comparison', 'children'),
     Output('commute_green_percentile_comparison', 'children'),
     Output('avg_sunny_days_percentile_comparison', 'children'),
     Output('avg_annual_temp_percentile_comparison', 'children'),
     Output('avg_winter_temp_percentile_comparison', 'children'),
     Output('avg_summer_temp_percentile_comparison', 'children'),
     Output('avg_winter_temp_comparison', 'children'),
     Output('avg_summer_temp_comparison', 'children'),
     Output('avg_fall_temp_percentile_comparison', 'children'),
     Output('avg_spring_temp_percentile_comparison', 'children'),
     Output('avg_fall_temp_comparison', 'children'),
     Output('avg_spring_temp_comparison', 'children'), 
     
     Output('pop_in_mvmt_only_us_comparison', 'children'),
     Output('pop_in_mvmt_only_us_percentile_comparison', 'children'),
     Output('pop_out_mvmt_only_us_comparison', 'children'),
     Output('pop_out_mvmt_only_us_percentile_comparison', 'children'),
     Output('pop_net_mvmt_only_us_comparison', 'children'),
     Output('pop_net_mvmt_only_us_percentile_comparison', 'children'),
     Output('pop_net_mvmt_only_us_percent_of_pop_comparison', 'children'),
     Output('pop_net_mvmt_only_us_percent_of_pop_percentile_comparison', 'children'),
     
     Output('poppct_urban_comparison', 'children'),
     Output('poppct_rural_comparison', 'children'),
     Output('areapct_urban_comparison', 'children'),
     Output('areapct_rural_comparison', 'children'),
     Output('poppct_urban_percentile_comparison', 'children'),
     Output('poppct_rural_percentile_comparison', 'children'),
     Output('areapct_urban_percentile_comparison', 'children'),
     Output('areapct_rural_percentile_comparison', 'children'),
     Output('popden_urban_comparison', 'children'),
     Output('popden_rural_comparison', 'children'),
     Output('popden_urban_percentile_comparison', 'children'),
     Output('popden_rural_percentile_comparison', 'children'),

     Output('tot_area_sqmi_comparison', 'children'),
     Output('tot_area_sqmi_percentile_comparison', 'children'),
     
     Output('combined_fips_comparison', 'children'),
     Output('county_name_comparison', 'children'),
     Output('state_name_comparison', 'children'),
     Output('csa_name_comparison', 'children'),
     Output('division_name_comparison', 'children'),
     Output('region_name_comparison', 'children'),
     
     Output('similar_counties_0_comparison', 'children'),
     Output('similar_counties_1_comparison', 'children'),
     Output('similar_counties_2_comparison', 'children'),
     Output('similar_counties_3_comparison', 'children'),
     Output('similar_counties_4_comparison', 'children'),
     
     Output('housing_occupied_perc_comparison', 'children'),
     Output('housing_occupied_percentile_comparison', 'children'),
     Output('housing_vacancy_perc_comparison', 'children'),
     Output('housing_vacancy_percentile_comparison', 'children'),
     Output('owner_perc_comparison', 'children'),
     Output('owner_percentile_comparison', 'children'),
     Output('renter_perc_comparison', 'children'),
     Output('renter_percentile_comparison', 'children') 
     ],
    [Input('state_dropdown_comparison', 'value'),
     Input('county_dropdown_comparison', 'value')])
def callback_a_comparison(selected_state, selected_county):
    if selected_state is not None and selected_county is not None and selected_state in dropdowns_list_dict_names and selected_county in dropdowns_list_dict_names[selected_state]:
        df_metrics_filtered = df_metrics[(df_metrics['state_name']==selected_state) & (df_metrics['county_name']==selected_county)]
        df_similar_counties_filtered = df_similar_counties[(df_similar_counties['state_name']==selected_state) & (df_similar_counties['county_name']==selected_county)].sort_values(['rank']).reset_index()

        
        name = df_metrics_filtered.iloc[0]['combined_name']
        unemp = df_metrics_filtered.iloc[0]['unemployment_perc']
        inc_HH = df_metrics_filtered.iloc[0]['median_hh_income']
        inc_capita = df_metrics_filtered.iloc[0]['per_capita_income']
        poverty = df_metrics_filtered.iloc[0]['poverty_perc']
        age = df_metrics_filtered.iloc[0]['median_age']
        political_lean = df_metrics_filtered.iloc[0]['political_lean']
        commute_time_in_min = df_metrics_filtered.iloc[0]['commute_time_in_min']
        bach_and_higher = df_metrics_filtered.iloc[0]['edu_bachelors_and_higher_perc']
        avg_sunny_days = df_metrics_filtered.iloc[0]['avg_sunny_days']
        avg_annual_temp = df_metrics_filtered.iloc[0]['avg_annual_temp']
     #   unemployment_rank = df_metrics_filtered.iloc[0]['unemployment_rank']
        unemployment_percentile = df_metrics_filtered.iloc[0]['unemployment_percentile']
        median_hh_income_percentile = df_metrics_filtered.iloc[0]['median_hh_income_percentile']
        poverty_percentile = df_metrics_filtered.iloc[0]['poverty_percentile']
        per_capita_income_percentile = df_metrics_filtered.iloc[0]['per_capita_income_percentile']
        median_age_percentile = df_metrics_filtered.iloc[0]['median_age_percentile']
        edu_bachelors_and_higher_percentile = df_metrics_filtered.iloc[0]['edu_bachelors_and_higher_percentile']
        commute_time_in_min_percentile = df_metrics_filtered.iloc[0]['commute_time_in_min_percentile']
        tot_pop = df_metrics_filtered.iloc[0]['tot_pop']
        tot_pop_percentile = df_metrics_filtered.iloc[0]['tot_pop_percentile']
        commute_green_perc = df_metrics_filtered.iloc[0]['commute_green_perc']
        commute_green_percentile = df_metrics_filtered.iloc[0]['commute_green_percentile']
        avg_sunny_days_percentile = df_metrics_filtered.iloc[0]['avg_sunny_days_percentile']
        avg_annual_temp_percentile = df_metrics_filtered.iloc[0]['avg_annual_temp_percentile']
        avg_winter_temp_percentile = df_metrics_filtered.iloc[0]['avg_winter_temp_percentile']
        avg_summer_temp_percentile = df_metrics_filtered.iloc[0]['avg_summer_temp_percentile']
        avg_winter_temp = df_metrics_filtered.iloc[0]['avg_winter_temp']
        avg_summer_temp = df_metrics_filtered.iloc[0]['avg_summer_temp']
        avg_fall_temp_percentile = df_metrics_filtered.iloc[0]['avg_fall_temp_percentile']
        avg_spring_temp_percentile = df_metrics_filtered.iloc[0]['avg_spring_temp_percentile']
        avg_fall_temp = df_metrics_filtered.iloc[0]['avg_fall_temp']
        avg_spring_temp = df_metrics_filtered.iloc[0]['avg_spring_temp']        
        pop_in_mvmt_only_us = df_metrics_filtered.iloc[0]['pop_in_mvmt_only_us']
        pop_in_mvmt_only_us_percentile = df_metrics_filtered.iloc[0]['pop_in_mvmt_only_us_percentile']
        pop_out_mvmt_only_us = df_metrics_filtered.iloc[0]['pop_out_mvmt_only_us']
        pop_out_mvmt_only_us_percentile = df_metrics_filtered.iloc[0]['pop_out_mvmt_only_us_percentile']
        pop_net_mvmt_only_us = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us']
        pop_net_mvmt_only_us_percentile = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us_percentile']
        pop_net_mvmt_only_us_percent_of_pop = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us_percent_of_pop']
        pop_net_mvmt_only_us_percent_of_pop_percentile = df_metrics_filtered.iloc[0]['pop_net_mvmt_only_us_percent_of_pop_percentile']

        poppct_urban = df_metrics_filtered.iloc[0]['poppct_urban']
        poppct_rural = df_metrics_filtered.iloc[0]['poppct_rural']
        areapct_urban = df_metrics_filtered.iloc[0]['areapct_urban']
        areapct_rural = df_metrics_filtered.iloc[0]['areapct_rural']
        poppct_urban_percentile = df_metrics_filtered.iloc[0]['poppct_urban_percentile']
        poppct_rural_percentile = df_metrics_filtered.iloc[0]['poppct_rural_percentile']
        areapct_urban_percentile = df_metrics_filtered.iloc[0]['areapct_urban_percentile']
        areapct_rural_percentile = df_metrics_filtered.iloc[0]['areapct_rural_percentile']
        popden_urban = df_metrics_filtered.iloc[0]['popden_urban']
        popden_rural = df_metrics_filtered.iloc[0]['popden_rural']
        popden_urban_percentile = df_metrics_filtered.iloc[0]['popden_urban_percentile']
        popden_rural_percentile = df_metrics_filtered.iloc[0]['popden_rural_percentile']

        tot_area_sqmi = df_metrics_filtered.iloc[0]['tot_area_sqmi']
        tot_area_sqmi_percentile = df_metrics_filtered.iloc[0]['tot_area_sqmi_percentile']
        
        combined_fips = df_metrics_filtered.iloc[0]['combined_fips']
        county_name = df_metrics_filtered.iloc[0]['county_name']
        state_name = df_metrics_filtered.iloc[0]['state_name']
        csa_name = df_metrics_filtered.iloc[0]['csa_name']
        division_name = df_metrics_filtered.iloc[0]['division_name']
        region_name = df_metrics_filtered.iloc[0]['region_name'] 
        
        similar_counties_0 = df_similar_counties_filtered.iloc[0]['similar_combined_name']
        similar_counties_1 = df_similar_counties_filtered.iloc[1]['similar_combined_name']
        similar_counties_2 = df_similar_counties_filtered.iloc[2]['similar_combined_name']
        similar_counties_3 = df_similar_counties_filtered.iloc[3]['similar_combined_name']
        similar_counties_4 = df_similar_counties_filtered.iloc[4]['similar_combined_name']
        
        housing_occupied_perc = df_metrics_filtered.iloc[0]['housing_occupied_perc']
        housing_occupied_percentile = df_metrics_filtered.iloc[0]['housing_occupied_percentile']
        housing_vacancy_perc = df_metrics_filtered.iloc[0]['housing_vacancy_perc']
        housing_vacancy_percentile = df_metrics_filtered.iloc[0]['housing_vacancy_percentile']
        owner_perc = df_metrics_filtered.iloc[0]['owner_perc']
        owner_percentile = df_metrics_filtered.iloc[0]['owner_percentile']
        renter_perc = df_metrics_filtered.iloc[0]['renter_perc']
        renter_percentile = df_metrics_filtered.iloc[0]['renter_percentile']    

        
        return name, \
                ' vs. ', \
                "{0:.1f}%".format(unemp), \
                '${:,.0f}'.format(inc_HH), \
                '${:,.0f}'.format(inc_capita), \
                "{0:.1f}%".format(poverty), \
                age, \
                political_lean, \
                str(int(commute_time_in_min)) + " min", \
                str(ord(int(unemployment_percentile*100))) + " pctl", \
                "{0:.1f}%".format(bach_and_higher), \
                avg_sunny_days, \
                str(int(avg_annual_temp)) + " degrees", \
                str(ord(int(median_hh_income_percentile*100))) + " pctl", \
                str(ord(int(poverty_percentile*100))) + " pctl", \
                str(ord(int(per_capita_income_percentile*100))) + " pctl", \
                str(ord(int(median_age_percentile*100))) + " pctl", \
                str(ord(int(edu_bachelors_and_higher_percentile*100))) + " pctl", \
                str(ord(int(commute_time_in_min_percentile*100))) + " pctl", \
                '{:,}'.format(tot_pop), \
                str(ord(int(tot_pop_percentile*100))) + " pctl", \
                "{0:.1f}%".format(commute_green_perc*100), \
                str(ord(int(commute_green_percentile*100))) + " pctl", \
                str(ord(int(avg_sunny_days_percentile*100))) + " pctl", \
                str(ord(int(avg_annual_temp_percentile*100))) + " pctl", \
                str(ord(int(avg_winter_temp_percentile*100))) + " pctl", \
                str(ord(int(avg_summer_temp_percentile*100))) + " pctl", \
                str(int(avg_winter_temp)) + " degrees", \
                str(int(avg_summer_temp)) + " degrees", \
                str(ord(int(avg_fall_temp_percentile*100))) + " pctl", \
                str(ord(int(avg_spring_temp_percentile*100))) + " pctl", \
                str(int(avg_fall_temp)) + " degrees", \
                str(int(avg_spring_temp)) + " degrees", \
                '{:,.0f}'.format(pop_in_mvmt_only_us), \
                str(ord(int(pop_in_mvmt_only_us_percentile*100))) + " pctl", \
                '{:,.0f}'.format(pop_out_mvmt_only_us), \
                str(ord(int(pop_out_mvmt_only_us_percentile*100))) + " pctl", \
                '{:,.0f}'.format(pop_net_mvmt_only_us), \
                str(ord(int(pop_net_mvmt_only_us_percentile*100))) + " pctl", \
                "{0:.1f}%".format(pop_net_mvmt_only_us_percent_of_pop*100), \
                str(ord(int(pop_net_mvmt_only_us_percent_of_pop_percentile*100))) + " pctl", \
                "{0:.2f}%".format(poppct_urban), \
                "{0:.2f}%".format(poppct_rural), \
                "{0:.2f}%".format(areapct_urban), \
                "{0:.2f}%".format(areapct_rural), \
                str(ord(int(poppct_urban_percentile*100))) + " pctl", \
                str(ord(int(poppct_rural_percentile*100))) + " pctl", \
                str(ord(int(areapct_urban_percentile*100))) + " pctl", \
                str(ord(int(areapct_rural_percentile*100))) + " pctl", \
                '{0:,.2f}'.format(popden_urban), \
                '{0:,.2f}'.format(popden_rural), \
                str(ord(int(popden_urban_percentile*100))) + " pctl", \
                str(ord(int(popden_rural_percentile*100))) + " pctl", \
                '{0:,.2f}'.format(tot_area_sqmi), \
                str(ord(int(tot_area_sqmi_percentile*100))) + " pctl", \
                str(combined_fips), \
                county_name, \
                state_name, \
                csa_name, \
                division_name, \
                region_name, \
                similar_counties_0, \
                similar_counties_1, \
                similar_counties_2, \
                similar_counties_3, \
                similar_counties_4, \
                "{0:.2f}%".format(housing_occupied_perc), \
                str(ord(int(housing_occupied_percentile*100))) + " pctl", \
                "{0:.2f}%".format(housing_vacancy_perc), \
                str(ord(int(housing_vacancy_percentile*100))) + " pctl", \
                "{0:.2f}%".format(owner_perc), \
                str(ord(int(owner_percentile*100))) + " pctl", \
                "{0:.2f}%".format(renter_perc), \
                str(ord(int(renter_percentile*100))) + " pctl"

    else:
            return [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]




#
#@app.callback(
#    [Output(component_id='element-to-hide', component_property='style')],
#    [Input('state_dropdown_comparison', 'value'),
#     Input('county_dropdown_comparison', 'value')])
#def hide_comparison_header_name(selected_state, selected_county):
#    if selected_state is not None and selected_county is not None:
#        return {'display': 'flex'}
#    else:
#        return {'display': 'none'} 

def build_page_header():
        page_header = html.Div(
        children=[
                html.H4(
                children='Market Maven',
                style={
                        'color': 'rgba(0, 0, 0, 0.8)',
                        'float': 'left', 
                        'display': 'inline-block',
                        'font-family': "Arial",
                        'font-size': '36px',
                        'font-weight': 'bold',
                        'margin': '0 0 15px 0',
                        'position': 'relative'
                        }
                ),
                html.Div(
                children=[
                        html.Ul(
                        children=[
                                html.Li(
                                children=[
                                        dcc.Link(
                                        children='Map',
                                        href='/',
                                        style={'text-decoration': 'none'}
                                        )], 
                                style={
                                        'display': 'inline-block', 
                                        'padding-left': '25px'
                                }),
                                html.Li(
                                children=[
                                        dcc.Link(
                                        children='Details',
                                        href='/details',
                                        style={'text-decoration': 'none'}
                                        )], 
                                style={
                                        'display': 'inline-block', 
                                        'padding-left': '25px'
                                }),
                                html.Li(
                                children=[
                                        dcc.Link(
                                        children='Clustering',
                                        href='/clustering',
                                        style={'text-decoration': 'none'}
                                        )], 
                                style={
                                        'display': 'inline-block', 
                                        'padding-left': '25px'
                                }),
                                html.Li(
                                children=[
                                        dcc.Link(
                                        children='Data Dictionary',
                                        href='/dictionary',
                                        style={'text-decoration': 'none'}
                                        )], 
                                style={
                                        'display': 'inline-block', 
                                        'padding-left': '25px'
                                })
                        ],
                        style={
                                'font-family': 'Arial',
                                'font-size': '18px',
                                'list-style-type': 'none', 
                                'margin': '0'}
                        )
                ],
                style={
                        'display': 'inline-block',
                        # 'float': 'right', 
                        'margin': '15px 0 0 25px', 
                        'overflow': 'hidden',
                }
                )
                
        ],
        className='page_header',
        id='page_header',
        style={'text-align': 'right', 'height': '40px', 'padding': '25px'}
        )

        return page_header

def build_details_layout(combined_fips='34021'):
        selected_county, selected_state = fips_to_name(combined_fips)
        details_layout = html.Div(children=[
        
        html.Div(children=[build_page_header()]),
        
        html.Div([
        html.Div(children=[
                html.Div([
                
                        html.Div('Highlighted County',style={'text-align':'left', 'font-weight': 'bold'}),
                
                        dcc.Dropdown(
                        id='state_dropdown',
                        options=[{'label': i, 'value': i} for i in df_metrics.state_name.unique()],
                        value=selected_state, #default
                        style={'width':'80%','font-style': 'italic'},
                        clearable=True
                        ),
        
                        dcc.Dropdown(
                        id='county_dropdown',
                        options=[{'label': i, 'value': i} for i in df_metrics.county_name.unique()],
                        value=selected_county, #default
                        style={'width':'80%','font-style': 'italic'},
                        clearable=True
                        ),    
                        ],
                                style={'display':'flex', 'flex-direction': 'column', 'width':'20%'},
                ),
        
                html.Div([
                
                        html.H1(children='Market Maven',style={'text-align':'center', 'visibility': 'hidden'}),
                        
                        html.H5([
                                html.Div(
                                        id='name_sel',style={'text-align':'center', 'padding': '0px 25px 25px 25px', 'width':'45%'}, children=get_metric('combined_name', selected_state=selected_state, selected_county=selected_county)
                                        ),
                                html.Div(
                                        id='vs_comparison',style={'text-align':'center', 'padding': '0px 25px 25px 25px', 'font-style': 'italic', 'color':'gray', 'width':'10%'}#, 'display':'none'}
                                        ),
                                html.Div(
                                        id='name_sel_comparison',style={'text-align':'center', 'padding': '0px 25px 25px 25px', 'font-style': 'italic', 'color':'gray', 'width':'45%'}
                                        ),
        #                            html.Div([
        #                                    html.Div(
        #                                        html.Div(
        #                                                id='name_sel_comparison',style={'text-align':'center', 'padding': '0px 25px 25px 25px', 'font-style': 'italic', 'color':'gray', 'width':'45%'}
        #                                                ),      
        #                                            id = 'element-to-hide'
        #                                            )],
        #                                    style= {'display': 'flex'} 
        #                                    )
                                
                                ],
                                style={'display':'flex', 'justify-content':'space-between'}
                                )
                                
                                
                        ],
                        style={'width':'60%'},
                ),         
        
                html.Div([
                        html.Div('Comparison County',style={'text-align':'left', 'font-weight': 'bold'}),
                        
                        dcc.Dropdown(
                                id='state_dropdown_comparison',
                                options=[{'label': i, 'value': i} for i in df_metrics.state_name.unique()],
                                #value='New Jersey', #default
                                style={'width':'80%','font-style': 'italic', 'float':'right'},
                                clearable=True,
                                placeholder="Select a state"
                                ),
                
                        dcc.Dropdown(
                                id='county_dropdown_comparison',
                                options=[{'label': i, 'value': i} for i in df_metrics.county_name.unique()],
                                #value='Mercer County', #default
                                style={'width':'80%','font-style': 'italic', 'float':'right'},
                                clearable=True,
                                placeholder="Select a county"
                                ),    
                        ],
                                style={'display':'flex', 'flex-direction': 'column', 'width':'20%', 'align-items':'flex-end'},
                ), 
        
        ],
        id="header_container",
        className="row header-container-display",
        ),

        html.Div([
                html.Div([
                html.H5(
                        "Economy",
                        id="Economy_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['Per Capita Income'], style={'font-weight': 'bold'}),
                                                html.Td(id='per_cap_inc', children=[get_metric(metric='per_capita_income', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='per_cap_inc_comparison', className="comparison_text"),
                                                html.Td(id='per_capita_income_percentile', children=[get_metric(metric='per_capita_income_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='per_capita_income_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Median Household Income'], style={'font-weight': 'bold'}), 
                                                html.Td(id='median_hh_inc', children=[get_metric(metric='median_hh_income', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='median_hh_inc_comparison', className="comparison_text"),
                                                html.Td(id='median_hh_income_percentile', children=[get_metric(metric='median_hh_income_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='median_hh_income_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Unemployment Rate'], style={'font-weight': 'bold'}), 
                                                html.Td(id='unemp_rt', children=[get_metric(metric='unemployment_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='unemp_rt_comparison', className="comparison_text"),
                                                html.Td(id='unemployment_percentile', children=[get_metric(metric='unemployment_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='unemployment_percentile_comparison', className="comparison_text")
                                        ]
                                        ),    
                                html.Tr(
                                        [
                                                html.Td(['Poverty Rate'], style={'font-weight': 'bold'}), 
                                                html.Td(id='poverty', children=[get_metric(metric='poverty_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='poverty_comparison', className="comparison_text"),
                                                html.Td(id='poverty_percentile', children=[get_metric(metric='poverty_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='poverty_percentile_comparison', className="comparison_text")
                                        ]
                                        ),       
                                ],
                                id="Economy_table",
                                className="center"
                                )
                ],
                id="Economy_container",
                className="pretty_container_two_cols",
                ),
                html.Div([
                html.H5(
                        "Social",
                        id="Social_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['Median Age'], style={'font-weight': 'bold'}),
                                                html.Td(id='age', children=[get_metric(metric='median_age', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='age_comparison', className="comparison_text"),
                                                html.Td(id='median_age_percentile', children=[get_metric(metric='median_age_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='median_age_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                
                                html.Tr(
                                        [
                                                html.Td(['Bachelors & Higher'], style={'font-weight': 'bold'}), 
                                                html.Td(id='bach_and_higher', children=[get_metric(metric='edu_bachelors_and_higher_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='bach_and_higher_comparison', className="comparison_text"),
                                                html.Td(id='edu_bachelors_and_higher_percentile', children=[get_metric(metric='edu_bachelors_and_higher_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='edu_bachelors_and_higher_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Green Commute'], style={'font-weight': 'bold'}), 
                                                html.Td(id='commute_green', children=[get_metric(metric='commute_green_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='commute_green_comparison', className="comparison_text"),
                                                html.Td(id='commute_green_percentile', children=[get_metric(metric='commute_green_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='commute_green_percentile_comparison', className="comparison_text")
                                        ]
                                        ),    
                                html.Tr(
                                        [
                                                html.Td(['Commute Time'], style={'font-weight': 'bold'}), 
                                                html.Td(id='commute_time_in_min', children=[get_metric(metric='commute_time_in_min', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='commute_time_in_min_comparison', className="comparison_text"),
                                                html.Td(id='commute_time_in_min_percentile', children=[get_metric(metric='commute_time_in_min_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='commute_time_in_min_percentile_comparison', className="comparison_text")
                                        ]
                                        ),     
                                html.Tr(
                                        [
                                                html.Td(['Political Lean'], style={'font-weight': 'bold'}), 
                                                html.Td(id='political_lean', children=[get_metric(metric='political_lean', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='political_lean_comparison', className="comparison_text"),
                                                html.Td(), 
                                                html.Td()
                                        ]
                                        ),
                                ],
                                id="Social_table",
                                className="center"
                                )
                ],
                id="Social_container",
                className="pretty_container_two_cols",
                ),    
        ],
        id="economy_social_container",
        className="row container-display",
        ),              
                                
        html.Div([
                html.Div([
                html.H5(
                        "Weather (statewide)",
                        id="Weather_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['Average Sunny Days'], style={'font-weight': 'bold'}),
                                                html.Td(id='avg_sunny_days', children=[get_metric(metric='avg_sunny_days', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_sunny_days_comparison', className="comparison_text"),
                                                html.Td(id='avg_sunny_days_percentile', children=[get_metric(metric='avg_sunny_days_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_sunny_days_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Average Annual Temperature'], style={'font-weight': 'bold'}), 
                                                html.Td(id='avg_annual_temp', children=[get_metric(metric='avg_annual_temp', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_annual_temp_comparison', className="comparison_text"),
                                                html.Td(id='avg_annual_temp_percentile', children=[get_metric(metric='avg_annual_temp_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_annual_temp_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Average Winter Temperature'], style={'font-weight': 'bold'}), 
                                                html.Td(id='avg_winter_temp', children=[get_metric(metric='avg_winter_temp', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_winter_temp_comparison', className="comparison_text"),
                                                html.Td(id='avg_winter_temp_percentile', children=[get_metric(metric='avg_winter_temp_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_winter_temp_percentile_comparison', className="comparison_text")
                                        ]
                                        ),    
                                html.Tr(
                                        [
                                                html.Td(['Average Spring Temperature'], style={'font-weight': 'bold'}), 
                                                html.Td(id='avg_spring_temp', children=[get_metric(metric='avg_spring_temp', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_spring_temp_comparison', className="comparison_text"),
                                                html.Td(id='avg_spring_temp_percentile', children=[get_metric(metric='avg_spring_temp_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_spring_temp_percentile_comparison', className="comparison_text")
                                        ]
                                        ), 
                                html.Tr(
                                        [
                                                html.Td(['Average Summer Temperature'], style={'font-weight': 'bold'}), 
                                                html.Td(id='avg_summer_temp', children=[get_metric(metric='avg_summer_temp', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_summer_temp_comparison', className="comparison_text"),
                                                html.Td(id='avg_summer_temp_percentile', children=[get_metric(metric='avg_summer_temp_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_summer_temp_percentile_comparison', className="comparison_text")
                                        ]
                                        ), 
                                html.Tr(
                                        [
                                                html.Td(['Average Fall Temperature'], style={'font-weight': 'bold'}), 
                                                html.Td(id='avg_fall_temp', children=[get_metric(metric='avg_fall_temp', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_fall_temp_comparison', className="comparison_text"),
                                                html.Td(id='avg_fall_temp_percentile', children=[get_metric(metric='avg_fall_temp_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='avg_fall_temp_percentile_comparison', className="comparison_text")
                                        ]
                                        ),       
                                ],
                                id="Weather_table",
                                className="center"
                                )
                ],
                id="Weather_container",
                className="pretty_container_two_cols",
                ),
                html.Div([
                html.H5(
                        "Population",
                        id="Population_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['Total Population'], style={'font-weight': 'bold'}),
                                                html.Td(id='tot_pop', children=[get_metric(metric='tot_pop', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='tot_pop_comparison', className="comparison_text"),
                                                html.Td(id='tot_pop_percentile', children=[get_metric(metric='tot_pop_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='tot_pop_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                
                                html.Tr(
                                        [
                                                html.Td(['Population Ins'], style={'font-weight': 'bold'}), 
                                                html.Td(id='pop_in_mvmt_only_us', children=[get_metric(metric='pop_in_mvmt_only_us', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_in_mvmt_only_us_comparison', className="comparison_text"),
                                                html.Td(id='pop_in_mvmt_only_us_percentile', children=[get_metric(metric='pop_in_mvmt_only_us_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_in_mvmt_only_us_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Population Outs'], style={'font-weight': 'bold'}), 
                                                html.Td(id='pop_out_mvmt_only_us', children=[get_metric(metric='pop_out_mvmt_only_us', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_out_mvmt_only_us_comparison', className="comparison_text"),
                                                html.Td(id='pop_out_mvmt_only_us_percentile', children=[get_metric(metric='pop_out_mvmt_only_us_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_out_mvmt_only_us_percentile_comparison', className="comparison_text")
                                        ]
                                        ), 
                                html.Tr(
                                        [
                                                html.Td(['Population Net Movement'], style={'font-weight': 'bold'}), 
                                                html.Td(id='pop_net_mvmt_only_us', children=[get_metric(metric='pop_net_mvmt_only_us', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_net_mvmt_only_us_comparison', className="comparison_text"),
                                                html.Td(id='pop_net_mvmt_only_us_percentile', children=[get_metric(metric='pop_net_mvmt_only_us_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_net_mvmt_only_us_percentile_comparison', className="comparison_text")
                                        ]
                                        ),   
                                html.Tr(
                                        [
                                                html.Td(['Net Movement as % of pop'], style={'font-weight': 'bold'}), 
                                                html.Td(id='pop_net_mvmt_only_us_percent_of_pop', children=[get_metric(metric='pop_net_mvmt_only_us_percent_of_pop', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_net_mvmt_only_us_percent_of_pop_comparison', className="comparison_text"),
                                                html.Td(id='pop_net_mvmt_only_us_percent_of_pop_percentile', children=[get_metric(metric='pop_net_mvmt_only_us_percent_of_pop_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='pop_net_mvmt_only_us_percent_of_pop_percentile_comparison', className="comparison_text")
                                        ]
                                        ),  
                                ],
                                id="population_table",
                                className="center"
                                )
                ],
                id="Population_container",
                className="pretty_container_two_cols",
                ),    
        ],
        id="weather_population_container",
        className="row container-display",
        ),                        
                                
        html.Div([
                html.Div([
                html.H5(
                        "Urban/Rural",
                        id="UrbanRural_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['Total Area (sq. mi.)'], style={'font-weight': 'bold'}),
                                                html.Td(id='tot_area_sqmi', children=[get_metric(metric='tot_area_sqmi', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='tot_area_sqmi_comparison', className="comparison_text"),
                                                html.Td(id='tot_area_sqmi_percentile', children=[get_metric(metric='tot_area_sqmi_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='tot_area_sqmi_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                
                                html.Tr(
                                        [
                                                html.Td(['Population % Urban'], style={'font-weight': 'bold'}),
                                                html.Td(id='poppct_urban', children=[get_metric(metric='poppct_urban', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='poppct_urban_comparison', className="comparison_text"),
                                                html.Td(id='poppct_urban_percentile', children=[get_metric(metric='poppct_urban_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='poppct_urban_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Population % Rural'], style={'font-weight': 'bold'}),
                                                html.Td(id='poppct_rural', children=[get_metric(metric='poppct_rural', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='poppct_rural_comparison', className="comparison_text"),
                                                html.Td(id='poppct_rural_percentile', children=[get_metric(metric='poppct_rural_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='poppct_rural_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Area % Urban'], style={'font-weight': 'bold'}),
                                                html.Td(id='areapct_urban', children=[get_metric(metric='areapct_urban', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='areapct_urban_comparison', className="comparison_text"),
                                                html.Td(id='areapct_urban_percentile', children=[get_metric(metric='areapct_urban_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='areapct_urban_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Area % Rural'], style={'font-weight': 'bold'}),
                                                html.Td(id='areapct_rural', children=[get_metric(metric='areapct_rural', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='areapct_rural_comparison', className="comparison_text"),
                                                html.Td(id='areapct_rural_percentile', children=[get_metric(metric='areapct_rural_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='areapct_rural_percentile_comparison', className="comparison_text")
                                        ]
                                        ),     
                                html.Tr(
                                        [
                                                html.Td(['Population Density Urban'], style={'font-weight': 'bold'}),
                                                html.Td(id='popden_urban', children=[get_metric(metric='popden_urban', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='popden_urban_comparison', className="comparison_text"),
                                                html.Td(id='popden_urban_percentile', children=[get_metric(metric='popden_urban_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='popden_urban_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Population Density Rural'], style={'font-weight': 'bold'}),
                                                html.Td(id='popden_rural', children=[get_metric(metric='popden_rural', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='popden_rural_comparison', className="comparison_text"),
                                                html.Td(id='popden_rural_percentile', children=[get_metric(metric='popden_rural_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='popden_rural_percentile_comparison', className="comparison_text")
                                        ]
                                        ),  
                                ],
                                id="UrbanRural_table",
                                className="center"
                                )
                ],
                id="UrbanRural_container",
                className="pretty_container_two_cols",
                ),
                html.Div([
                html.H5(
                        "Geography",
                        id="Geography_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['FIPS Code'], style={'font-weight': 'bold'}), 
                                                html.Td(id='combined_fips', children=[get_metric(metric='combined_fips', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='combined_fips_comparison', className="comparison_text"),
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['County'], style={'font-weight': 'bold'}), 
                                                html.Td(id='county_name', children=[get_metric(metric='county_name', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='county_name_comparison', className="comparison_text"),
                                        ]
                                        ), 
                                html.Tr(
                                        [
                                                html.Td(['State'], style={'font-weight': 'bold'}), 
                                                html.Td(id='state_name', children=[get_metric(metric='state_name', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='state_name_comparison', className="comparison_text"),
                                        ]
                                        ), 
                                html.Tr(
                                        [
                                                html.Td(['CSA'], style={'font-weight': 'bold'}), 
                                                html.Td(id='csa_name', children=[get_metric(metric='csa_name', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='csa_name_comparison', className="comparison_text"),
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Division'], style={'font-weight': 'bold'}), 
                                                html.Td(id='division_name', children=[get_metric(metric='division_name', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='division_name_comparison', className="comparison_text"),
                                        ]
                                        ),                        
                                html.Tr(
                                        [
                                                html.Td(['Region'], style={'font-weight': 'bold'}), 
                                                html.Td(id='region_name', children=[get_metric(metric='region_name', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='region_name_comparison', className="comparison_text"),
                                        ]
                                        ),                            ],
                                id="geography_table",
                                className="center"
                                )
                ],
                id="Geography_container",
                className="pretty_container_two_cols",
                ),    
        ],
        id="urbanrural_geography_container",
        className="row container-display",
        ),                         
                                
        html.Div([
                html.Div([
                html.H5(
                        "Real Estate",
                        id="RealEstate_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(['Housing % Occupied'], style={'font-weight': 'bold'}),
                                                html.Td(id='housing_occupied_perc', children=[get_metric(metric='housing_occupied_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='housing_occupied_perc_comparison', className="comparison_text"),
                                                html.Td(id='housing_occupied_percentile', children=[get_metric(metric='housing_occupied_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='housing_occupied_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Housing % Vacancies'], style={'font-weight': 'bold'}),
                                                html.Td(id='housing_vacancy_perc', children=[get_metric(metric='housing_vacancy_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='housing_vacancy_perc_comparison', className="comparison_text"),
                                                html.Td(id='housing_vacancy_percentile', children=[get_metric(metric='housing_vacancy_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='housing_vacancy_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Housing % Owned'], style={'font-weight': 'bold'}),
                                                html.Td(id='owner_perc', children=[get_metric(metric='owner_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='owner_perc_comparison', className="comparison_text"),
                                                html.Td(id='owner_percentile', children=[get_metric(metric='owner_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='owner_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(['Housing % Rented'], style={'font-weight': 'bold'}),
                                                html.Td(id='renter_perc', children=[get_metric(metric='renter_perc', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='renter_perc_comparison', className="comparison_text"),
                                                html.Td(id='renter_percentile', children=[get_metric(metric='renter_percentile', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='renter_percentile_comparison', className="comparison_text")
                                        ]
                                        ),
                                ],
                                id="RealEstate_table",
                                className="center"
                                )
                ],
                id="RealEstate_container",
                className="pretty_container_two_cols",
                ),
                html.Div([
                html.H5(
                        "Similar Counties",
                        id="SimilarCounties_title", 
                        className="section_title"
                        ),
                html.Table(
                        [
                                html.Tr(
                                        [
                                                html.Td(id='similar_counties_0', children=[get_metric(metric='similar_combined_name_0', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='similar_counties_0_comparison', className="comparison_text"),
                                        ]
                                        ),
                                html.Tr(
                                        [
                                                html.Td(id='similar_counties_1', children=[get_metric(metric='similar_combined_name_1', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='similar_counties_1_comparison', className="comparison_text"),
                                        ]
                                        ),                        html.Tr(
                                        [
                                                html.Td(id='similar_counties_2', children=[get_metric(metric='similar_combined_name_2', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='similar_counties_2_comparison', className="comparison_text"),

                                        ]
                                        ),                        html.Tr(
                                        [
                                                html.Td(id='similar_counties_3', children=[get_metric(metric='similar_combined_name_3', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='similar_counties_3_comparison', className="comparison_text"),

                                        ]
                                        ),                        html.Tr(
                                        [
                                                html.Td(id='similar_counties_4', children=[get_metric(metric='similar_combined_name_4', selected_state=selected_state, selected_county=selected_county)]), 
                                                html.Td(id='similar_counties_4_comparison', className="comparison_text"),

                                        ]
                                        ),
                                html.Tr(
                                        html.Td(colSpan=2, rowSpan=2, children=[
                                                html.Button(children=[dcc.Link(
                                                        children=f'Find more similar counties', 
                                                        # href=f'/clustering?fips={combined_fips}', 
                                                        href=f'/clustering', 
                                                        style={'font-weight': 'bold', 'text-decoration': 'none'})
                                                ])], style={'text-align': 'center'})
                                                
                                        )
                                ],
                                id="SimilarCounties_table",
                                className="center"
                                )
                ],
                id="SimilarCounties_container",
                className="pretty_container_two_cols",
                ),    
        ],
        id="RealEstate_SimilarCounties_container",
        className="row container-display",
        ),               
        ], style={'background-color': '#fdfdfd'})])

        return details_layout


def ord(n):
  s = ('th', 'st', 'nd', 'rd') + ('th',)*10
  v = n%100
  if v > 13:
    return f'{n}{s[v%10]}'
  else:
    return f'{n}{s[v]}'