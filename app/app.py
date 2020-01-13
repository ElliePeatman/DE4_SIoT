import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy
import datetime
from requests import get
import datetime
import json
import os
import numpy as np
from numpy.random import normal, seed
from API import dark_sky2

print('Initialising.. running Dash version:', dcc.__version__)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
print('1')
All_D = pd.read_csv('data_new.csv')
All_D = All_D[['CTime Days','CTime Mins','Cloud Cover','Wind Speed','Outside Temperature','Outside Humidity','Precip Intensity','Inside Temperature','Inside Humidity','Day','Timestamp','Hours','Minutes','Seconds','AMPM','Datetime']]

with open('Weather_Credentials.json') as f:
        weatherCreds = json.load(f)
data_l = dark_sky2(weatherCreds['darksky_key'])
cloud_now = str(data_l[0])
wind_now = str(0.01*data_l[1])
temp_now = str((data_l[2]-32)/(5/9))
hum_now = str(data_l[3])
rain_now = str(0.001*data_l[4])


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='This Week', value='tab-1'),
        dcc.Tab(label='My House', value='tab-2'),
        dcc.Tab(label='Live Data', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1(children='Weather in Beverley, Yorkshire this week'),
            html.H5(children='If you do not live in Yorkshire, too bad! More locations coming soon..'),
            html.H6(children='Click on a label to make that variable disappear!'),
            html.Div([
                dcc.Graph(
                    figure=dict(
                        
                        data=[
                            dict(
                                x=All_D['Datetime'],
                                y=All_D['Cloud Cover'],
                                type='line',
                                name='Cloud Cover',
                                marker=dict(
                                    color='rgb(55, 118, 100)'
                                )
                            ),
                            dict(
                                x=All_D['Datetime'],
                                y=All_D['Outside Temperature'],
                                type='line',
                                name='Outside Temperature',
                                marker=dict(
                                    color='rgb(26, 118, 255)'
                                )
                            ),
                            dict(
                                x=All_D['Datetime'],
                                y=All_D['Wind Speed'],
                                type='line',
                                name='Wind Speed',
                                marker=dict(
                                    color='rgb(26, 0, 255)'
                                )
                            ),
                            dict(
                                x=All_D['Datetime'],
                                y=All_D['Precip Intensity'],
                                type='line',
                                
                                name='Precip Intensity',
                                marker=dict(
                                    color='rgb(200, 10, 10)'
                                )
                            )
                        ],
                        layout=dict(
                            title='Weather Indicators and Outside Temperature',
                            showlegend=True,
                            legend=dict(
                                x=0,
                                y=1.0
                            ) 
                        )
                    ),
                    style={'display': 'inline-block', 'width': '100%', 'height': '100%'}), 
            ]),

            
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H2('Does the Temperature Outside My House Affect My Central Heating?'),
                html.H5(children='No, no it does not.'),
                html.H6(children='Click on a label to make that variable disappear!'),
                html.Div([
                    dcc.Graph(
                        figure=dict(
                            
                            data=[
                                dict(
                                    x=All_D['Datetime'],
                                    y=All_D['Inside Temperature'],
                                    type='line',
                                    name='Inside Temperature',
                                    marker=dict(
                                        color='rgb(200, 50, 100)'
                                    )
                                ),
                                dict(
                                    x=All_D['Datetime'],
                                    y=All_D['Outside Temperature'],
                                    type='line',
                                    name='Outside Temperature',
                                    marker=dict(
                                        color='rgb(250, 118, 0)'
                                    )
                                )
                            ],
                            layout=dict(
                                title='Temperature Inside and Outside Your House',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                
                            )
                        ),
                        style={'display': 'inline-block', 'width': '100%', 'height': '100%'}), 
                ]),
                
                html.H2('What about the Humidity Inside and Outside Your House?'),
                html.H5(children='Very low regression values here :('),
                html.H6(children='Click on a label to make that variable disappear!'),
                html.Div([
                    dcc.Graph(
                        figure=dict(
                            
                            data=[
                                dict(
                                    x=All_D['Datetime'],
                                    y=All_D['Inside Humidity'],
                                    type='line',
                                    name='Inside Humidity',
                                    marker=dict(
                                        color='rgb(55, 200, 100)'
                                    )
                                ),
                                dict(
                                    x=All_D['Datetime'],
                                    y=All_D['Outside Humidity'],
                                    type='line',
                                    name='Outside Humidity',
                                    marker=dict(
                                        color='rgb(26, 150, 170)'
                                    )
                                )
                            ],
                            layout=dict(
                                title='Humidity Inside and Outside Your House',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                
                            )
                        ),
                        style={'display': 'inline-block', 'width': '100%', 'height': '100%'}), 
                ]) 
        ]) 
    
    
    elif tab == 'tab-3':
        return html.Div([
                html.H1('Live Data From Dark Sky API'),
                html.H3('Hit refresh for the most up to date readings..'),
                
                html.Table([ 
                    html.Tr([html.Th(['Clouds at']), html.Td(cloud_now), html.Td(['% today'])]),
                    html.Tr([html.Th(['Wind Speeds of']), html.Td(wind_now), html.Td(['mph today'])]),
                    html.Tr([html.Th(['Temperatures soaring to:']), html.Td(temp_now), html.Td(['Degrees Celcius today'])]),
                    html.Tr([html.Th(['Humidity is']), html.Td(hum_now), html.Td(['% today'])]),
                    html.Tr([html.Th(['Current rainfall:']), html.Td(rain_now), html.Td(['mm today'])])]),
            ])
        
                    
               
            

    

if __name__ == '__main__':
    app.run_server(debug=True)

            