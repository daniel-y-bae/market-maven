# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.express as px

import pandas as pd
import numpy as np
from scipy import stats

import sqlite3

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import KNNImputer
from sklearn.neighbors import KDTree

from app import app

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_data():
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "assets", "market_maven.sqlite"))
    raw_data = pd.read_sql("select * from metrics_no_percentiles_v", conn)
    conn.close()

    # dropping columns that are just names or identifiers
    numeric_data = raw_data.select_dtypes(exclude="object")

    # imputing missing values based on nearest neighbors instead of deleting them
    imp = KNNImputer(n_neighbors=10, weights="distance")
    numeric_imputed = pd.DataFrame(imp.fit_transform(numeric_data), columns=numeric_data.columns)

    # removing extreme outliers
    # documentation says RobustScaler handles outliers but there was data for Rio Arriba county New Mexico and
    # Loving county Texas that were too extreme so using StandardScaler and handling outliers manually
    outliers = numeric_imputed[(np.abs(stats.zscore(numeric_imputed)) >= 50).all(axis=1)].index
    if len(outliers) != 0:
        numeric_ex_outlier = numeric_imputed.drop(outliers).reset_index()
        full_ex_outlier = raw_data.drop(outliers).reset_index()
    else:
        numeric_ex_outlier = numeric_imputed
        full_ex_outlier = raw_data
    
    county_state = full_ex_outlier[["county_fips","state_fips","county_name","state_name","combined_fips","combined_name"]]

    scaler = StandardScaler().fit(numeric_ex_outlier) 
    scaled_data = scaler.transform(numeric_ex_outlier)

    reduced_data = PCA(n_components=2).fit_transform(scaled_data)
    return reduced_data, county_state

def create_kmeans_model(data, n):
    kmeans = KMeans(n_clusters=n, n_init=10, max_iter=300, random_state=0).fit(data)
    return kmeans

def find_nearest_neighbors(data, n):
    neighbors = KDTree(data, leaf_size=40)
    dist, ind = neighbors.query(data, k=n+1)
    return dist, ind

model_data, names = get_data()
kmeans_model = create_kmeans_model(model_data, 60)
neighbors_dist, neighbors_ind = find_nearest_neighbors(model_data, 30)

model_data_df = pd.DataFrame(model_data, columns=["x","y"])
model_data_df["cluster_number"] = kmeans_model.labels_
fig = px.scatter(model_data_df,
                 x=model_data_df["x"], y=model_data_df["y"],
                 color=model_data_df["cluster_number"],
                 hover_name=names[["county_name","state_name"]].apply(", ".join, axis=1),
                 hover_data={"x":False, "y":False},
                 custom_data=[names.index],
                 color_continuous_scale=px.colors.sequential.Aggrnyl,
                 log_x=True,
                 log_y=True,
                 range_x=[.01,40],
                 range_y=[.01,40])

fig.update_layout(
    font_color="#181818",
    coloraxis_showscale=False,
    paper_bgcolor="#181818",
    plot_bgcolor="#181818"
)

fig.update_xaxes(showgrid=False, zeroline=False)
fig.update_yaxes(showgrid=False, zeroline=False)

fig.update_traces(marker_symbol="star-diamond",
                  marker={"size":5},
                  selector={"mode":'markers'})


# def fips_to_name(fips):
#         county_name = names[names['combined_fips'] == str(fips)]['county_name'].values[0]
#         state_name = names[names['combined_fips'] == str(fips)]['state_name'].values[0]
#         return county_name, state_name

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



def build_cluster_layout(combined_fips='01001'):
    # selected_county, selected_state = fips_to_name(combined_fips)
    INSTRUCTION_BOX_HEADER_STYLE_1 = {
        'color': 'rgba(88, 88, 88, 1)',
        'font-family': 'Arial',
        'font-size': '12px',
        'font-weight': 'bold',
        'padding': '0 0 5px 0',
        'margin': '0px'
    }

    INSTRUCTION_BOX_STYLE_1 = {
        'background-color': 'rgba(255, 255, 255, 1)',
        'border': '1px solid rgba(200, 200, 200, 1)',
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

    def build_instructions_box():
        INSTRUCTION_BOX_CONTENT_STYLE_1 = {
            'color': 'rgba(88, 88, 88, 1)',
            'font-family': 'Arial',
            'font-size': '12px',
        }

        children = dcc.Markdown("""
    * Select a county, either by clicking on a point or using the drop downs on the top right.
    * The selected county will have a darker color.
    * The closer a county is to your selection, the more similar they are.
    * Reset to default using the 'RESET' button on the top left.
    """)
        return html.P(
            children=[children],
            className='instruction_box_content',
            id='instruction_box_content',
            style=INSTRUCTION_BOX_CONTENT_STYLE_1
        )

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

    cluster_layout = html.Div(children=[

    html.Div(children=[build_page_header()]),

    html.Div(children=[instruction_box]),



    html.Div(style={"background-color":"rgb(24, 24, 24)", "color":"white", "width":"100%", "height":"100vh"}, children=[
        html.Div(style={"background-color":"rgb(24, 24, 24)"}, children=[
            html.Div(children=[
                html.Button("Reset", id="reset", 
                style={"position":"absolute", "display":"inline-block", "color":"white"})
            ], style={"padding": "15px 0 0 15px"})
        ]),

        html.Div(children=[
            # html.H1(
            #     id="title",
            #     children="Market Maven",
            #     style={"textAlign":"center"}
            # ),

            html.Div(
                id="selection",
                children="Clustered Counties", 
                style={"textAlign": "center"}
            )
        ], style={"margin":"auto", "height": "50px", "padding-top": "10px"}),

        html.Div(children=[      
            html.Div(children=[
                dcc.Dropdown(
                    id="state",
                    options=[{"label":x, "value":x} for x in names["state_name"].unique()],
                    placeholder="Select a state",
                    # value=selected_state,
                    style={"color":"black"}
                )
            ]),

            html.Div(children=[
                dcc.Dropdown(
                    id="county",
                    placeholder="Select a county",
                    # value=selected_county,
                    style={"color":"black"}
                )
            ])
        ], style={"margin-right": "15px", "position":"absolute", "top":"105px", "right":"0", "width":"20%"}),

        dcc.Loading(id="loading", children=[
            dcc.Graph(
                id='cluster',
                animate=False,
                figure=fig,
                style={"height":"90vh", "margin": "25px 15px 0 0"}
            )
    ], style={"background-color":"#181818"})
    ])])

    return cluster_layout

@app.callback(
    [Output(component_id="selection", component_property="children"),
     Output(component_id="cluster", component_property="figure")],
    [Input(component_id="cluster", component_property="clickData"),
     Input(component_id="reset", component_property="n_clicks"),
     Input(component_id="state", component_property="value"),
     Input(component_id="county", component_property="value")]
)
def update_cluster(selection, reset_clicks, state_value, county_value):
    if selection is None and (state_value is None or county_value is None):
        raise PreventUpdate

    def create_new_fig(ind):
        neighbors = neighbors_ind[ind]
        distances = np.around(neighbors_dist[ind], decimals=2)
        neighborhood = pd.DataFrame(model_data[neighbors][:,:2], columns=["x", "y"])
        neighborhood["difference"] = distances
        neighbor_names = names[["county_name","state_name"]].iloc[neighbors].apply(", ".join, axis=1)

        new_fig = px.scatter(neighborhood,
                x=neighborhood["x"], y=neighborhood["y"],
                color=neighborhood["difference"],
                hover_name=neighbor_names,
                hover_data={"x":False, "y":False},
                custom_data=[neighbor_names.index],
                color_continuous_scale=px.colors.sequential.Aggrnyl)

        new_fig.update_layout(
            font_color="#181818",
            coloraxis_showscale=False,
            paper_bgcolor="#181818",
            plot_bgcolor="#181818"
        )

        new_fig.update_xaxes(showgrid=False, zeroline=False)
        new_fig.update_yaxes(showgrid=False, zeroline=False)
        
        new_fig.update_traces(marker_symbol="diamond",
                              marker={"size":20,
                                      "line":{"width":2,
                                              "color":"white"}},
                              selector={"mode":'markers'})
        
        return neighbor_names[ind], new_fig

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "reset" in changed_id:
        selection_name = "Clustered Counties"
        new_fig = fig
    elif "county" in changed_id:
        county_ind = names.index[(names["state_name"] == state_value) & (names["county_name"] == county_value)][0]
        selection_name, new_fig = create_new_fig(county_ind)
    elif "cluster" in changed_id:
        county_ind = selection["points"][0]["customdata"][0]
        selection_name, new_fig = create_new_fig(county_ind)
    else:
        raise PreventUpdate

    return selection_name, new_fig

@app.callback(
    Output(component_id="county", component_property="options"),
    Input(component_id="state", component_property="value")
)
def update_county_dropdown(state_name):
    if state_name is None:
        raise PreventUpdate

    filtered_df = names[names["state_name"] == state_name]
    county_options = [{"label": x, "value":x} for x in filtered_df["county_name"]]

    return county_options