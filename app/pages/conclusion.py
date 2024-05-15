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
            html.P(children=[
                html.Strong("Key findings:"),
                html.P(children="1. The coastal nations order more from the DEAD company"), 
                html.P(children="  - Amn, Baldur's Gate and Calimshan are the top 3 nations by the amount of orders "),
                html.P(children="2. Lack of seasonaly trend in orders "),
                html.P(children="3. The anomaly in delivery time during June 2021 and onward (explained in the report)")
            ], style = {"width":"25cm"}),
            html.Br(),
            html.Strong("Conclusions based on our three guiding questions:"),
            html.P(children=""),
            html.P(children=[
                html.Strong("1. How can we visualize the delivery times across the regions of Faerun to find areas of improvement in shipping times for the DEAD company?"),
                html.P(children="For this question, we have to look at the bar chart of the Avearge Delivery Time by Nation in Visualization Plot 1. In the chart, we see that Estagund has the lowest average delivery time of 8.7 days, while Mintarn has the highest average delivery time of 11 days even though the amount of orders is not that high. Similar problem of longer average delivery time with relatively low amount of orders can be found in Blingdenstone with almost average 11 days of delivery. "),
                html.Br(),
                html.Strong("2. What is the best way to map out the best and worst selling products sold by the DEAD company?"),
                html.P(children="To answer this question, we have to look at the bar chart of Sales by Subtype of all nations in Visualization Plot 1. The chart clearly ranks the subtypes of product from the best sales to the worst sales. The subtype of product that has the best sales is Magic Utility with 467.281k of sales, following by Martial Melee Weapon with 437.763k of sales. These are the two main subtypes that are relatively dominant in the rank On the other side, vehicle has the worst sales among all the subtypes with only 7836 of sales. The other subtype that can be found at the bottom is Percussion Instrument with amlost 12k of sales."),
                html.Br(),
                html.Strong("3. How can we gauge the popularity of the DEAD company across the regions of the Forgotten Realms?"),
                html.P(children="To answer this question, we have to combine the findings and the answers of the two previous questions. Based on the first finding, we would suggest DEAD comanpy to come out some marketing strategies targeting on those nations that are not closed to the coast to boost the sales in those areas than those coastal nations. Based on the first guiding question, we think DEAD company should try to find out the reasons cause the longer delivery time in Mintarn and Blingdenstone since the orders from these two nations are not relatively high among all nations and put some measures to fix the problem and imrpove the delivery time. The last suggestion from us is that the company can lauch some sales promotions on those subtype of products that have worse sales. ")
            ])
        ], style={"width":"25cm"})
    ]),
    html.Br()
])
