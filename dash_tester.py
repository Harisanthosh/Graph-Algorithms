# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

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
app.layout = html.Div(style={'backgroundColor': colors['background'],'color': colors['text'], 'textAlign': 'center'},children=[
    html.Img(src=app.get_asset_url('emden_leer.png'),style={
                'height': '50%',
                'width': '50%'
            }),
    html.H1(children='Neo4j & Dash'),

    html.Div(children='''
        NeoDash: A web application framework for Python customized for Python and Neo4j.
    '''),
    html.Br(),
    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # ),
    # html.H4(children='US Agriculture Exports (2011)'),
    # generate_table(df),
    dcc.Dropdown(
            id='my-dropdown',
            style={'color': '#D4AF37'},
            options=[
                {'label': 'Page Rank Algorithm', 'value': 'PR'},
                {'label': 'Closeness Centrality', 'value': 'CR'},
                {'label': 'Betweenness Centrality', 'value': 'BR'},
                {'label': 'Harmonic Centrality', 'value': 'HR'}
            ],
            value='PR'
        ),
    html.Br(),
    html.Button('Test Neo4j', id='button_neo',style={'color': '#D4AF37'}),
    html.Br(),
    html.Div(style={'textAlign': 'center'},id="load_div", children='loading..')

])

@app.callback(dash.dependencies.Output('load_div','children'),[dash.dependencies.Input('my-dropdown', 'value'),dash.dependencies.Input('button_neo', 'n_clicks')])
def update_output(value, n_clicks):
    # value = dash.dependencies.Input('my-dropdown', 'value')
    print(f'The button was clicked {n_clicks} times and the algorithm selected is {value}')
    if (value == "PR"):
        resp = requests.get('http://localhost:8000/getrank').json()
    elif (value == "CR"):
        resp = requests.get('http://localhost:8000/getcentrality').json()
    elif (value == "BR"):
        resp = requests.get('http://localhost:8000/betweennesscentrality').json()
    elif (value == "HR"):
        resp = requests.get('http://localhost:8000/harmoniccentrality').json()
    else:
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