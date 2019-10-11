# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_json_table(jsondata, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(val) for key,val in jsondata.items()])]

        # Body
        # [html.Tr([
        #     html.Td(jsondata[i][val]) for key,val in jsondata.items()
        # ]) for i in range(min(len(jsondata), max_rows))]
    )
app.layout = html.Div(children=[
    html.H1(children='Neo4j & Dash'),

    html.Div(children='''
        NeoDash: A web application framework for Python customized for Python and Neo4j.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df),
    html.Button('Run Neo4j', id='button_neo'),
    html.Div(id="load_div", children='loading..')

])

@app.callback(dash.dependencies.Output('load_div','children'),[dash.dependencies.Input('button_neo', 'n_clicks')])
def update_output(n_clicks):
    print(f'The button was clicked {n_clicks} times')
    resp = requests.get('http://localhost:8000/getrank').json()
    print(resp)
    respjson = pd.DataFrame(resp)
    print(respjson)
    # return 'The button was clicked {} times and the response is {}'.format(
    #     n_clicks,
    #     generate_table(respjson)
    # )
    return generate_table(respjson)

if __name__ == '__main__':
    app.run_server(debug=True)