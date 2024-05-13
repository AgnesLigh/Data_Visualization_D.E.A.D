import dash
from dash import Dash, html, dcc, callback
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

pagename='Visualization plot 2'

dash.register_page(__name__,
                   path='/Plot_2',
                   title=pagename,
                   name=pagename,
                   order=2)


# 示例数据
df = pd.read_csv("https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/orders_nation_season.csv")
subtype_order = pd.read_csv("https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/subtype_order_month.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"],format="%d/%m/%Y")
df["DeliveryDate"] = pd.to_datetime(df["OrderDate"],format="%d/%m/%Y")

order_counts = df["OrderDate"].value_counts().reset_index()
order_counts.columns = ["OrderDate", "Number of Orders"]
order_counts = order_counts.sort_values("OrderDate")

delivery_counts = df["DeliveryDate"].value_counts().reset_index()
delivery_counts.columns = ["DeliveryDate", "Number of Deliveries"]
delivery_counts = delivery_counts.sort_values("DeliveryDate")

average_delivery_time = df.groupby('OrderDate')['DeliveryTime'].mean().reset_index()

subtype_fig = px.bar(subtype_order, x='OrderMonth', y='Counts', color='Subtype', 
                     color_continuous_scale= "Viridis", title='Order Counts by Subtype and Date')

subtype_fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})


layout= dbc.Container([
  dbc.Row([
        html.Div([
            html.H3(children="To explore the relationship between 'when' and 'what' "),
            html.P("This plot aims to find possible relationship between ...")
        ], style={"width":"20cm"})
    ]),
    html.Br(),
  dbc.Row([
    html.Div([
    dcc.Dropdown(
        id='date-type-picker',
        options=["Order Date", "Delivery Date", "Average Delivery Time"],
        value="Order Date",
        clearable=False,  
        style={'width': '50%'}
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=order_counts['OrderDate'].min(),
        end_date=delivery_counts['DeliveryDate'].max(),
        display_format='YYYY-MM-DD')
    ])]),
    html.Div([
        dcc.Graph(id='sales-bar-chart')
    ]),
    html.Div([
        dcc.Graph(id='subtype-bar-chart',figure=subtype_fig)
    ])
])

# Callback to update the graph based on the selected date type and date range
@callback(
    Output('sales-bar-chart', 'figure'),
    [Input('date-type-picker', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_date_type, start_date, end_date):

    if selected_date_type == 'Order Date':
        mask = (order_counts['OrderDate'] >= start_date) & (order_counts['OrderDate'] <= end_date)
        filtered_order_counts = order_counts.loc[mask]
        
        fig = px.bar(filtered_order_counts, x='OrderDate', y='Number of Orders', title='Orders by Date')
        

    elif selected_date_type == 'Delivery Date':
        mask = (delivery_counts['DeliveryDate'] >= start_date) & (delivery_counts['DeliveryDate'] <= end_date)
        filtered_delivery_counts = delivery_counts.loc[mask]
        
        fig = px.bar(filtered_delivery_counts, x='DeliveryDate', y='Number of Deliveries', title='Deliveries by Date')

    elif selected_date_type == 'Average Delivery Time':
        mask = (average_delivery_time['OrderDate'] >= start_date) & (average_delivery_time['OrderDate'] <= end_date)
        filtered_average_delivery_time = average_delivery_time.loc[mask]
        
        fig = px.bar(filtered_average_delivery_time, x='OrderDate', y='DeliveryTime', title='Average Delivery Time by Date',
                     labels={'DeliveryTime': 'Average Delivery Time'})

    return fig


