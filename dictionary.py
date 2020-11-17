#!/usr/bin/env python
# coding: utf-8

import os

import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import sqlite3

from app import app

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect(os.path.join(ROOT_DIR, 'assets', 'market_maven.sqlite'))
df_data_dict = pd.read_sql_query(''' select * from data_dict''', conn)

def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# layout for global page header (application title, etc.)
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
        style={'text-align': 'right', 'height': '40px', 'padding': '25px 42px 25px 25px'}
        )

        return page_header

dictionary_layout = html.Div(children=[
    html.Div(children=[build_page_header()]),

    html.Div(children=[
    dcc.Tabs([
        dcc.Tab(label='Economy', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Economy"])
          
        ]),
        dcc.Tab(label='Social', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Social"])
            
            
        ]),
        dcc.Tab(label='Weather', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Weather"])
            
        ]),
        
        dcc.Tab(label='Population', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Population"])
            
        ]),
        
        dcc.Tab(label='Urban/Rural', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Urban/Rural"])
            
        ]),
        
        dcc.Tab(label='Real Estate', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Real Estate"])
            
        ]),
        
        
        dcc.Tab(label='Geography', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Geography"])
            
        ]),
        
        dcc.Tab(label='Similar Counties', children=[
            generate_table(df_data_dict[df_data_dict["Category"] == "Similar Counties"])
            
        ])]),        
    ])
])