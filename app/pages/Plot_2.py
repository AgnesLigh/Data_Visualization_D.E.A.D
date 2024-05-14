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
subtype_order = pd.read_csv("https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/subtype_order_date.csv")
subtype_delivery = pd.read_csv("https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/subtype_delivery_date.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"],format="%d/%m/%Y")
df["DeliveryDate"] = pd.to_datetime(df["OrderDate"],format="%d/%m/%Y")

order_counts = df["OrderDate"].value_counts().reset_index()
order_counts.columns = ["OrderDate", "Number of Orders"]
order_counts = order_counts.sort_values("OrderDate")

delivery_counts = df["DeliveryDate"].value_counts().reset_index()
delivery_counts.columns = ["DeliveryDate", "Number of Deliveries"]
delivery_counts = delivery_counts.sort_values("DeliveryDate")

average_delivery_time = df.groupby('OrderDate')['DeliveryTime'].mean().reset_index()

subtype_order["OrderDate"] = pd.to_datetime(subtype_order["OrderDate"],format="%d/%m/%Y")
subtype_delivery["DeliveryDate"] = pd.to_datetime(subtype_delivery["DeliveryDate"],format="%d/%m/%Y")

layout= dbc.Container([
  dbc.Row([
        html.Div([
            html.H3(children="To explore the relationship between 'when' and 'what' "),
            html.P(children="In this page, you will find the visualization of the order and delivery related information. There are mainly two parts of the visualization."),
            html.P(children="In the first part, we focus on 'when'. As you can find the amount of order and delivery at different time frame of your interest. Additionally, you can also see the average delivery time based on the two information above. For the time frame of your interest, you can first click and select in the calender for a general time frame. Then you can drag-select a more specific time frame to have a closer look at the fluctuation of order/delivery/average delivery time. (Small tip: if you double click on the bar chart of specific time frame, you can go back to the general time frame selected from calender) ")
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
        min_date_allowed=order_counts['OrderDate'].min(),
        max_date_allowed=delivery_counts['DeliveryDate'].max(),
        start_date='2019-01-01',
        end_date='2023-12-31',
        display_format='YYYY-MM-DD')
    ])]),
    html.Div([
        dcc.Graph(id='sales-bar-chart')
    ]),
    dbc.Row([
        html.Div([
            html.P("For the second part, we combine 'when' and 'what'. You can see the whole distribution of all the subtypes of product within certain time frame of your choice. You can select a sepecfic subtype or few subtypes of interest to see the distribution. The drag-select function for a more specific time frame and the doubble-click resetting function can also be applied here. ")
        ], style={"width":"20cm"})
    ]),
    html.Br(),
    dbc.Row([
    html.Div([
    dcc.Dropdown(
        id='subtype-date-type-picker',
        options=["Order Date", "Delivery Date"],
        value="Order Date",
        clearable=False,  
        style={'width': '50%'}
    ),
    dcc.DatePickerRange(
        id='subtype-date-picker-range',
        min_date_allowed=order_counts['OrderDate'].min(),
        max_date_allowed=delivery_counts['DeliveryDate'].max(),
        start_date='2019-01-01',
        end_date='2019-12-31',
        display_format='YYYY-MM-DD')
    ])
    ]),
    html.Div([
        dcc.Graph(id='subtype-bar-chart')
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

# Callback to update the graph based on the selected date type and date range
@callback(
    Output('subtype-bar-chart', 'figure'),
    [Input('subtype-date-type-picker', 'value'),
     Input('subtype-date-picker-range', 'start_date'),
     Input('subtype-date-picker-range', 'end_date')]
)
def update_graph(selected_date_type, start_date, end_date):
    if selected_date_type == 'Order Date':
        mask = (subtype_order['OrderDate'] >= start_date) & (subtype_order['OrderDate'] <= end_date)
        filtered_subtype_order = subtype_order.loc[mask]
        fig = px.bar(filtered_subtype_order, x='OrderDate', y='Counts', color='Subtype', 
                 color_continuous_scale= "Viridis", title='Order Counts by Subtype and Date')

        fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

    elif selected_date_type == 'Delivery Date':
        mask = (subtype_delivery['DeliveryDate'] >= start_date) & (subtype_delivery['DeliveryDate'] <= end_date)
        filtered_subtype_delivery = subtype_delivery.loc[mask]
        fig = px.bar(filtered_subtype_delivery, x='DeliveryDate', y='Counts', color='Subtype', 
                 color_continuous_scale= "Viridis", title='Order Counts by Subtype and Date')

        fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

    return fig
