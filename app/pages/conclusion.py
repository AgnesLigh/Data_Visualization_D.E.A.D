import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

pagename='Conclusions'

dash.register_page(__name__,
                   path='/conclusion',
                   title=pagename,
                   name=pagename,
                   order=3)


layout= dbc.Container([
  dbc.Row([
        html.Div([
            html.H3(children="Conclusions and Key findings"),
            html.P(children="Our three guiding questions:"),
            html.P(children="1. How can we visualize the delivery times across the regions of Faerun to find areas of improvement in shipping times for the DEAD company?"),
            html.P(children="2. What is the best way to map out the best and worst selling products sold by the DEAD company?"),
            html.P(children="3. How can we gauge the popularity of the DEAD company across the regions of the Forgotten Realms?")
        ], style={"width":"20cm"})
    ]),
    html.Br()
])
