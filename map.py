# -*- coding: utf-8 -*-
"""
ADD DESCRIPTION
"""

import json
import os
import sqlite3

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
import requests

from app import app

# ==============================
# CONFIGURATION
# ==============================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS = {
    'db':               os.path.join(ROOT_DIR, 'assets', 'market_maven.sqlite'),
    'fips_states':      os.path.join(ROOT_DIR, 'assets', 'fips-states.json'),
    'geojson_counties': os.path.join('assets', 'geojson-counties.json'), # doesn't load when referencing ROOT_DIR, uh?
    'geojson_states':   os.path.join('assets', 'geojson-states.json') # doesn't load when referencing ROOT_DIR, uh?
}

PROPERTIES = {
    # ECONOMY
    'MEDIAN_HH_INCOME': {
        'classes': [0, 10000, 20000, 45000, 50000, 55000, 75000, 140000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'PER_CAPITA_INCOME': {
        'classes': [0, 10000, 15000, 20000, 25000, 30000, 35000, 73000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'UNEMPLOYMENT_PERC': {
        'classes': [0, 1, 2, 3, 3.5, 4.0, 11, 17],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POVERTY_PERC': {
        'classes': [0, 5, 7, 9, 11, 13, 15, 55],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    # SOCIAL
    'MEDIAN_AGE': {
        'classes': [20, 25, 30, 35, 40, 45, 50, 55],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'EDU_BACHELORS_AND_HIGHER_PERC': {
        'classes': [7, 14, 21, 28, 35, 42, 49, 56],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'COMMUTE_GREEN_PERC': {
        'classes': [0.0, 0.05, 0.11, 0.13, 0.15, 0.17, 0.20, 1.0],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'COMMUTE_TIME_IN_MIN': {
        'classes': [0, 5, 10, 15, 20, 25, 30, 35],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POLITICAL_SCALE': {
        'classes': [-1, -.6, -.4, -.2, -.1, .1, .2, .4, .6],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    # WEATHER
    'AVG_SUNNY_DAYS': { 
        'classes': [55, 65, 75, 85, 95, 105, 150, 200],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AVG_ANNUAL_TEMP': { 
        'classes': [25, 35, 40, 45, 50, 55, 65, 71],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AVG_FALL_TEMP': { 
        'classes': [25, 35, 40, 45, 50, 55, 60, 73],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AVG_WINTER_TEMP': {
        'classes': [0, 10, 20, 25, 35, 45, 55, 70],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AVG_SPRING_TEMP': {
        'classes': [20, 30, 40, 45, 50, 55, 65, 70],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AVG_SUMMER_TEMP': {
        'classes': [50, 55, 60, 65, 70, 75, 80, 82],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    # POPULATION
    'TOT_POP': {
        'classes': [0, 5000, 10000, 25000, 45000, 70000, 500000, 10100000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POP_IN_MVMT_ONLY_US': {
        'classes': [0, 300, 600, 1200, 1800, 3600, 10000, 208000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POP_OUT_MVMT_ONLY_US': {
        'classes': [0, 300, 600, 1200, 1800, 3600, 10000, 318000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POP_NET_MVMT_ONLY_US': {
        'classes': [-120000, -10000, -5000, -1000, -500, 500, 1000, 5000, 10000],
        'color_scale': [
            '#54A7CD',
            '#85CCE1',
            '#B7E4EF',
            '#EAEBCD',
            '#FFD78A',
            '#FFAF61',
            '#FF753D', 
            '#F3290B',
            '#B80012',
        ],
    },
    'POP_NET_MVMT_ONLY_US_PERCENT_OF_POP': {
        'classes': [-.4, -.05, -.01,  -.005, -.001, .001, .005, .01, .05],
        'color_scale': [
            '#54A7CD',
            '#85CCE1',
            '#B7E4EF',
            '#EAEBCD',
            '#FFD78A',
            '#FFAF61',
            '#FF753D', 
            '#F3290B',
            '#B80012',
        ],
    },
    # URBAN/RURAL
    'TOT_AREA_SQMI': {
        'classes': [0, 200, 400, 600, 800, 2000, 64000, 200000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POPPCT_URBAN': {
        'classes': [-0.1, 10, 30, 40, 50, 60, 70, 100.0],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POPPCT_RURAL': {
        'classes': [0, 10, 20, 30, 40, 50, 60, 100.0],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AREAPCT_URBAN': {
        'classes': [-0.1, 0.5, 0.9, 1.2, 1.5, 5.0, 40, 70],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'AREAPCT_RURAL': {
        'classes': [0, 80, 95, 96, 97, 98, 99, 100],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POPDEN_URBAN': {
        'classes': [0, 500, 1000, 1200, 1500, 1900, 3000, 70000],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'POPDEN_RURAL': {
        'classes': [0, 5, 15, 30, 60, 120, 240, 600],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    # REAL ESTATE
    'HOUSING_OCCUPIED_PERC': {
        'classes': [0, 55, 65, 75, 80, 85, 90, 95],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'HOUSING_VACANCY_PERC': {
        'classes': [0, 5, 10, 15, 20, 40, 60, 90],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'OWNER_PERC': {
        'classes': [0, 50, 55, 60, 65, 70, 75, 100],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
    'RENTER_PERC': {
        'classes': [0, 10, 15, 20, 25, 30, 45, 100],
        'color_scale': [
            '#FFEDA0', 
            '#FED976', 
            '#FEB24C', 
            '#FD8D3C', 
            '#FC4E2A', 
            '#E31A1C', 
            '#BD0026', 
            '#800026'
        ],
    },
}

METRICS_OPTIONS = [
    # ECONOMY
    {'label': 'Economy', 'value': '', 'disabled': True},
    {'label': 'Median Household Income', 'value': 'MEDIAN_HH_INCOME', 'disabled': False},
    {'label': 'Per Capita Income', 'value': 'PER_CAPITA_INCOME', 'disabled': False},
    {'label': 'Poverty Percentage', 'value': 'POVERTY_PERC', 'disabled': False},
    {'label': 'Unemployment Percentage', 'value': 'UNEMPLOYMENT_PERC', 'disabled': False},

    # POPULATION
    {'label': 'Population', 'value': '', 'disabled': True},
    {'label': 'Total Population', 'value': 'TOT_POP', 'disabled': False},
    {'label': 'Population Ins', 'value': 'POP_IN_MVMT_ONLY_US', 'disabled': False},
    {'label': 'Population Outs', 'value': 'POP_OUT_MVMT_ONLY_US', 'disabled': False},
    {'label': 'Population Net Movement', 'value': 'POP_NET_MVMT_ONLY_US', 'disabled': False},
    {'label': 'Net Movement as Percentage of Population', 'value': 'POP_NET_MVMT_ONLY_US_PERCENT_OF_POP', 'disabled': False},

    # REAL ESTATE
    {'label': 'Real Estate', 'value': '', 'disabled': True},
    {'label': 'Housing Occupied Percentage', 'value': 'HOUSING_OCCUPIED_PERC', 'disabled': False},
    {'label': 'Housing Vacancy Percentage', 'value': 'HOUSING_VACANCY_PERC', 'disabled': False},
    {'label': 'Housing Owned Percentage', 'value': 'OWNER_PERC', 'disabled': False},
    {'label': 'Housing Rented Percentage', 'value': 'RENTER_PERC', 'disabled': False},

    # SOCIAL
    {'label': 'Social', 'value': '', 'disabled': True},
    {'label': 'Bachelors Degree & Higher', 'value': 'EDU_BACHELORS_AND_HIGHER_PERC', 'disabled': False},
    {'label': 'Commute Time (in Minutes)', 'value': 'COMMUTE_TIME_IN_MIN', 'disabled': False},
    {'label': 'Green Commute Percentage', 'value': 'COMMUTE_GREEN_PERC', 'disabled': False},
    {'label': 'Median Age', 'value': 'MEDIAN_AGE', 'disabled': False},
    # {'label': 'Political Scale', 'value': 'POLITICAL_SCALE', 'disabled': False},

    # URBAN/RURAL
    {'label': 'Urban vs. Rural', 'value': '', 'disabled': True},
    {'label': 'Total Area (in Square Miles)', 'value': 'TOT_AREA_SQMI', 'disabled': False},
    {'label': 'Urban Population Percentage', 'value': 'POPPCT_URBAN', 'disabled': False},
    {'label': 'Rural Population Percentage', 'value': 'POPPCT_RURAL', 'disabled': False},
    {'label': 'Urban Area Percentage', 'value': 'AREAPCT_URBAN', 'disabled': False},
    {'label': 'Rural Area Percentage', 'value': 'AREAPCT_RURAL', 'disabled': False},
    {'label': 'Urban Population Density', 'value': 'POPDEN_URBAN', 'disabled': False},
    {'label': 'Rural Population Density', 'value': 'POPDEN_RURAL', 'disabled': False},

    # WEATHER
    {'label': 'Weather', 'value': '', 'disabled': True},
    {'label': 'Average Annual Temperature', 'value': 'AVG_ANNUAL_TEMP', 'disabled': False},
    {'label': 'Average Number of Sunny Days', 'value': 'AVG_SUNNY_DAYS', 'disabled': False},
    {'label': 'Average Spring Temperature', 'value': 'AVG_SPRING_TEMP', 'disabled': False},
    {'label': 'Average Summer Temperature', 'value': 'AVG_SUMMER_TEMP', 'disabled': False},
    {'label': 'Average Fall Temperature', 'value': 'AVG_FALL_TEMP', 'disabled': False},
    {'label': 'Average Winter Temperature', 'value': 'AVG_WINTER_TEMP', 'disabled': False}, 
]

# ==============================
# STYLES
# ==============================

COLOR_SCALE = [
    '#FFEDA0', 
    '#FED976', 
    '#FEB24C', 
    '#FD8D3C', 
    '#FC4E2A', 
    '#E31A1C', 
    '#BD0026', 
    '#800026'
]

COLOR_BOX_STYLE_1 = {
    'font-family': 'Arial',
    'font-size': '12px'
}

GEOJSON_COUNTIES_STYLE_1 = {
    'color': 'gray',
    'fillOpacity': 0.5,
    'opacity': 0.5,
    'weight': 1
}

GEOJSON_STATES_STYLE_1 = {
    'color': 'gray',
    'dashArray': '1',
    'fillOpacity': 0,
    'opacity': 1
}

GEOJSON_HOVER_STYLE_1 = {    
    'color': '#666',
    'dashArray': '',
    'weight': 5
}

GEOJSON_HOVER_STYLE_2 = {    
    'color': '#666',
    'dashArray': '',
    'weight': 5
}

INFO_BOX_STYLE_1 = {
    'display': 'none'
}

INFO_BOX_STYLE_2 = {
    'background-color': 'rgba(255, 255, 255, 0.85)',
    'border': '1px solid rgba(200, 200, 200, 0.85)',
    'border-radius': '5px',
    'display': 'block',
    'font-family': 'Arial',
    'font-size': '16px',
    'padding-left': '15px',
    'padding-right': '15px',
    'padding-top': '15px',
    'position': 'absolute',
    'right': '25px',
    'top': '35px',
    'z-index': '1000'
}

INFO_BOX_CONTENT_STYLE_1 = {
    'color': 'rgba(88, 88, 88, 1)',
    'font-family': 'Arial',
    'font-size': '11px'
}

INFO_BOX_HEADER_STYLE_1 = {
    'color': 'rgba(88, 88, 88, 1)',
    'font-family': 'Arial',
    'font-size': '18px',
    'font-weight': 'bold',
    'margin': '0px',
    'padding': '0px'
}

INFO_BOX_LINK_STYLE_1 = {
    'color': 'rgba(88, 88, 88, 1)',
    'font-family': 'Arial',
    'font-size': '14px',
    'font-style': 'italic'
}

INSTRUCTION_BOX_STYLE_1 = {
    'background-color': 'rgba(255, 255, 255, 0.85)',
    'border': '1px solid rgba(200, 200, 200, 0.85)',
    'border-radius': '5px',
    'bottom': '25px',
    'display': 'block',
    'font-family': 'Arial',
    'font-size': '16px',
    'left': '25px',
    'margin': '0px',
    'padding': '10px 15px 0 15px',
    'position': 'absolute',
    'z-index': '1000'
}

INSTRUCTION_BOX_CONTENT_STYLE_1 = {
    'color': 'rgba(88, 88, 88, 1)',
    'font-family': 'Arial',
    'font-size': '12px',
}

INSTRUCTION_BOX_HEADER_STYLE_1 = {
    'color': 'rgba(88, 88, 88, 1)',
    'font-family': 'Arial',
    'font-size': '12px',
    'font-weight': 'bold',
    'padding': '0 0 5px 0',
    'margin': '0px'
}

MAP_LAYOUT_STYLE_1 = {
    'display': 'block',
    'height': '94vh',
    'margin': 'auto',
    'position': 'relative',
    'width': '100%'
}

METRICS_DROPDOWN_STYLE_1 = {
    'font-family': 'Arial',
    'font-size': '16px',
    'left': '10px',
    'opacity': '0.9',
    'position': 'absolute',
    'top': '15px',
    'width': '400px',
    'z-index': '1000'
}

# ==============================
# GLOBALS
# ==============================

selected_county_name = None
selected_county_combined_fips = None
selected_state_name = None
# ==============================
# PRELOAD
# ==============================

# open fips to states translations 
with open(ASSETS['fips_states'], 'r') as json_file:
    FIPS_STATES_DICT = json.load(json_file)

# open database for read
conn = sqlite3.connect(ASSETS['db'])

try:
    db = pd.read_sql_query('''select * from metrics_v''', conn)
except:
    print(f'Error opening db: {ASSETS["db"]}')

conn.close()

# ==============================
# UTILITIES
# ==============================

def build_color_bar(classes, color_scale, width=550, height=30, position='bottomleft'):
    ctg = ['{:,}+'.format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ['{:,}+'.format(classes[-1])]
    color_bar = dlx.categorical_colorbar(
        categories=ctg, 
        colorscale=color_scale,
        height=height,  
        position=position,
        style=COLOR_BOX_STYLE_1,
        width=width)
    return color_bar

def build_geojson_counties(color_prop=None):
    id = 'geojson_counties'
    url = ASSETS['geojson_counties']
    zoomToBounds = False
    zoomToBoundsOnClick = False

    if color_prop:
        hideout = dict(
            classes=PROPERTIES[color_prop]['classes'], 
            color_prop=color_prop, 
            colorscale=PROPERTIES[color_prop]['color_scale'], 
            style=GEOJSON_COUNTIES_STYLE_1)
        # hoverStyle = GEOJSON_HOVER_STYLE_2
        hoverStyle = None
        options = dict(style=dlx.choropleth.style)
    else:
        hideout = dict()
        # hoverStyle = GEOJSON_HOVER_STYLE_1
        hoverStyle = None
        options = dict(style=GEOJSON_COUNTIES_STYLE_1)

    return dl.GeoJSON(
        hideout=hideout,
        id=id, 
        hoverStyle=hoverStyle,
        options=options,
        url=url,
        zoomToBounds=zoomToBounds,
        zoomToBoundsOnClick=zoomToBoundsOnClick
    )

def build_geojson_states():
    id = 'geojson_states'
    options = dict(style=GEOJSON_STATES_STYLE_1)
    url = ASSETS['geojson_states']
    zoomToBounds = False
    zoomToBoundsOnClick = False

    return dl.GeoJSON(
        id=id,
        options=options,
        zoomToBounds=zoomToBounds,
        zoomToBoundsOnClick=zoomToBoundsOnClick,
        url=url
    )

def build_info_box_content(county_combined_fips):
    data = read_metrics_from_db(county_combined_fips)
    children = dcc.Markdown(f"""
#### Economy
* __Per Capita Income:__ ${data['per_capita_income']:,}
* __Median Household Income:__ ${data['median_hh_income']:,}
* __Poverty Percentage:__ {data['poverty_perc']:.1f}%
* __Unemployment Percentage:__ {data['unemployment_perc']:.1f}%
#### Population
* __Total Population:__ {data['tot_pop']:,}
* __Population Ins:__ {data['pop_in_mvmt_only_us']:,.0f}
* __Population Outs:__ {data['pop_out_mvmt_only_us']:,.0f}
* __Population Net Movement:__ {data['pop_net_mvmt_only_us']:,.0f}
* __Net Movement (Percentage of Population):__ {data['pop_net_mvmt_only_us_percent_of_pop']:.3f}%
#### Real Estate
* __Housing Occupied Percentage:__ {data['housing_occupied_perc']:.1f}%
* __Housing Vacancy Percentage:__ {data['housing_vacancy_perc']:.1f}%
* __Housing Owned Percentage:__ {data['owner_perc']:.1f}%
* __Housing Rented Percentage:__ {data['renter_perc']:.1f}%
#### Social
* __Median Age:__ {data['median_age']:,.1f} years old
* __Bachelors Degree & Higher:__ {data['edu_bachelors_and_higher_perc']:.1f}%
* __Green Commute Percentage:__ {data['commute_green_perc']:.1f}%
* __Commute Time:__ {data['commute_time_in_min']:.1f} minutes
* __Political Lean:__ {data['political_scale']:.3f} ({convert_political_scale_to_lean(data['political_scale'])})
#### Urban vs. Rural
* __Total Area:__ {data['tot_area_sqmi']:,.1f} square miles
* __Urban Population Percentage:__ {data['poppct_urban']:.1f}%
* __Rural Population Percentage:__ {data['poppct_rural']:.1f}%
* __Urban Area Percentage:__ {data['areapct_urban']:.1f}%
* __Rural Population Percentage:__ {data['areapct_rural']:.1f}%
* __Urban Population Density:__ {data['popden_urban']:,}
* __Rural Population Density:__ {data['popden_rural']:,}
#### Weather
* __Average Annual Temperature:__ {int(data['avg_annual_temp']):,} &#8457;
* __Average Number of Sunny Days:__ {int(data['avg_sunny_days']):,} days
* __Average Spring Temperature:__ {int(data['avg_spring_temp']):,} &#8457;
* __Average Summer Temperature:__ {int(data['avg_summer_temp']):,} &#8457;
* __Average Fall Temperature:__ {int(data['avg_fall_temp']):,} &#8457;
* __Average Winter Temperature:__ {int(data['avg_winter_temp']):,} &#8457;
""")
    return html.P(
        children=[children],
        className='info_box_content',
        id='info_box_content',
        style=INFO_BOX_CONTENT_STYLE_1
    )

def build_info_box_header(county_name, state_name):
    children = f'{county_name} County ({state_name})'
    return html.P(
        children=[children],
        className='info_box_header',
        id='info_box_header',
        style=INFO_BOX_HEADER_STYLE_1
    )

def build_info_box_link(county_combined_fips=None):
    children = [
        'Click ', 
        dcc.Link(
            id='info_box_link_link', 
            className='info_box_link_link', 
            children=['here'], 
            href=f'/details?fips={county_combined_fips}',
            refresh=False), 
        ' to learn more details about this county.'
    ]

    return html.P(
        children=children,
        className='info_box_link',
        id='info_box_link',
        style=INFO_BOX_LINK_STYLE_1
    )

def build_instructions_box():
    children = dcc.Markdown("""
* Select a metric from the dropdown to visualize it on the map.
* Click on the 'x' icon within the dropdown to reset the map.
* Click on the gray sections of the map to select a county and open its details pane.
* Click anywhere off the gray sections of the map to remove the details pane.
""")
    return html.P(
        children=[children],
        className='instruction_box_content',
        id='instruction_box_content',
        style=INSTRUCTION_BOX_CONTENT_STYLE_1
    )

def convert_political_scale_to_lean(scale):
    if scale >= 0.1:
        return 'Solid Republican'
    elif scale >= 0.02 and scale < 0.1:
        return 'Lean Republican'
    elif scale >= -0.02 and scale < 0.02:
        return 'Toss-Up'
    elif scale >= -0.1 and scale < -0.02:
        return 'Lean Democrat'
    elif scale < -0.1:
        return 'Solid Democrat'
    else:
        return 'Unknown'

def fips_to_state(fips, fips_states_dict):
    try:
        state = fips_states_dict[fips]
    except:
        state = ''
    return state
    
def lat_lng_to_fips(click_lat_lng, lat=None, lng=None):
    if click_lat_lng:
        lat = click_lat_lng[0]
        lng = click_lat_lng[1]
    else:
        lat = lat
        lng = lng
    r = requests.get(f'https://geo.fcc.gov/api/census/area?lat={lat}&lon={lng}&format=json')
    data = r.json()
    county_combined_fips = None
    county_name = None
    state_name = None
    try:
        county_combined_fips = data["results"][0]["county_fips"]
        county_name = data["results"][0]["county_name"]
        state_name = data["results"][0]["state_name"]
    except:
        pass
    return county_combined_fips, county_name, state_name

def read_metrics_from_db(county_combined_fips=None):
    metrics = [metric.lower() for metric in PROPERTIES.keys()]
    data = {}
    for metric in metrics:
        value = db[db['combined_fips'] == county_combined_fips][metric].values[0]
        data[metric] = value
    return data

# ==============================
# LAYOUT
# ==============================

# layout for metrics dropdown input
dropdown = dcc.Dropdown(
    className='metrics_dropdown',
    clearable=True,
    id='dropdown', 
    options=METRICS_OPTIONS, 
    placeholder='Select a metric to visualize it on the map...', 
    style=METRICS_DROPDOWN_STYLE_1)

# layout for information pane with county details
info_box = html.Div(
    children=[build_info_box_header(selected_county_name, selected_state_name)],
    className='info_box',
    id='info_box',
    style=INFO_BOX_STYLE_1
)

# layout for application instructions pane
instruction_box = html.Div(
    children=[
        html.H4(
            className='instruction_box_header',
            children='Instructions',
            id='instruction_box_header',
            style=INSTRUCTION_BOX_HEADER_STYLE_1), 
        build_instructions_box()],
    className='instructions_box',
    id='instructions_box',
    style=INSTRUCTION_BOX_STYLE_1
)

# layout for geojson map
map = dl.Map(
    center=[37, -96],
    children=[dl.TileLayer(), build_geojson_counties(), build_geojson_states()],
    className='layout_map',
    id='layout_map',
    zoom=5 
)

# layout for global page header (application title, etc.)
page_header = html.Div(
    children=[
        html.H4(
            children='Market Maven',
            style={
                'color': 'rgba(0, 0, 0, 0.8)',
                'float': 'left', 
                'font-family': "Arial",
                'font-size': '36px',
                'font-weight': 'bold',
                'margin': '0 0 15px 0',
                'position': 'relative'}
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
                'float': 'right', 
                'margin': '15px 0 0 0', 
                'overflow': 'hidden', 
                'text-align': 'center'
            }
        )
        
    ],
    className='page_header',
    id='page_header',
    style={'height': '25px', 'padding': '25px'}
)

# layout for global map application page
map_layout = html.Div(
    className='map_layout',
    children=[
        html.Div(
            children=[page_header]
        ),
        html.Div(
            children=[
                map, 
                info_box, 
                instruction_box, 
                dropdown
            ], 
            style=MAP_LAYOUT_STYLE_1)
    ],
    id='map_layout')

# ==============================
# CALLBACKS
# ==============================

@app.callback(Output('geojson_counties', 'children'), [Input('geojson_counties', 'hover_feature')])
def map_hover(hover_feature):
    if hover_feature is not None:
        county = hover_feature['properties']['NAME']
        state = fips_to_state(hover_feature['properties']['STATE'], FIPS_STATES_DICT)
        content = f'{county} County'
        if state:
            content = content + f' ({state})'
        return dl.Tooltip(content)
    return None

@app.callback([Output('info_box', 'children'), Output('info_box', 'style')], [Input('layout_map', 'click_lat_lng')])
def update_info_box(click_lat_lng):
    county_combined_fips, county_name, state_name = lat_lng_to_fips(click_lat_lng)
    global selected_county_name
    selected_county_name = county_name
    global selected_state_name
    selected_state_name = state_name
    global selected_county_combined_fips
    selected_county_combined_fips = county_combined_fips
    style = INFO_BOX_STYLE_1
    header = None
    link = None
    content = None
    if selected_county_name is not None:
        style = INFO_BOX_STYLE_2
        header = build_info_box_header(selected_county_name, selected_state_name)
        link = build_info_box_link(county_combined_fips)
        content = build_info_box_content(selected_county_combined_fips)
    return [[header, link, content], style]

@app.callback([Output('layout_map', 'children')], [Input('dropdown', 'value')])
def update_map(value):
    children = [dl.TileLayer()]
    geojson_states = build_geojson_states()
    children.append(geojson_states)
    if value:
        classes = PROPERTIES[value]['classes']
        color_scale = PROPERTIES[value]['color_scale']
        color_bar = build_color_bar(classes, color_scale)
        children.append(color_bar)
        geojson_counties = build_geojson_counties(color_prop=value)
    else:
        geojson_counties = build_geojson_counties()
    children.append(geojson_counties)
    return [children]