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
            html.H3(children="To explore the relationship between 'where' and 'what' "),
            html.P("This plot aims to find possible relationship between ...")
        ], style={"width":"20cm"})
    ]),
    html.Br()
])
