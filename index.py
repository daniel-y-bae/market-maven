import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import cluster
import details
import dictionary
import map


app.title = 'Market Maven | Your real estate markets comparison tool'

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('url', 'search')])
def display_page(pathname, search):
    if pathname == '/':
        return map.map_layout
    elif pathname == '/details':
        if search:
            combined_fips = str(search.split('=')[1])
        else:
            combined_fips = '01001'
        return details.build_details_layout(combined_fips)
    elif pathname == '/clustering':
        return cluster.build_cluster_layout()
    elif pathname == '/dictionary':
        return dictionary.dictionary_layout
    else:
        return map.map_layout

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)