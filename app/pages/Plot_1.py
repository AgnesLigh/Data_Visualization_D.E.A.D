import dash
from dash import Dash, html, dcc, callback
import pandas as pd
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from PIL import Image, ImageOps
import json

pagename='Visualization plot 1'

dash.register_page(__name__,
                   path='/Plot_1',
                   title=pagename,
                   name=pagename,
                   order=1)



image_path = "https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/assets/map.png"
gray_image_path = "https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/assets/map.png"

df = pd.read_csv('https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/data_sample.csv')
subtype_count = pd.read_csv('https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/subtype_nation.csv')
sub_orders = pd.read_csv('https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/data/orders_territory.csv')


# Constants
img_width = 1600
img_height = 900
scale_factor = 0.7

# Dash Application Layout

layout= dbc.Container([
  dbc.Row([
        html.Div([
            html.H3(children="To explore the relationship between 'where' and 'what' "),
            html.P("This plot aims to find possible relationship between ...")
        ], style={"width":"20cm"})
    ]),
    html.Br(),
    dcc.Dropdown(
        id='option-dropdown',
        options=['Total orders', 'Total customers', 'Total cart price (CP)'],
        value='Total orders',  # 初始值
        clearable=False,  # 禁止清空
        style={'width': '50%'} ),
    html.Br(),
    dbc.Row([
        html.Div([
            dcc.Graph(id='map-graph')])
    ]),
    dbc.Row([
        html.Div([
            dcc.Graph(id='details-graph-pie-chart'),
            dcc.Graph(id='details-graph-territory-bar-chart')
            ], style={'display': 'flex', 'flex-direction': 'row'})  # CSS Flexbox)
    ]),
    dbc.Row([
        html.Div([
            dcc.Graph(id='details-graph-products-bar-chart')])
    ])
])



# callback function of pie chart
@callback(
    Output('details-graph-pie-chart', 'figure'),
    Input('map-graph', 'clickData')
)
def update_details(clickData):
    if clickData is None:
        all_values=[sum(df['Key Account']),sum(df['No Key Account']),
                    sum(df['Private Buyer'])]
        fig=px.pie(values=all_values, 
                     names=['Key Account','No Key Account','Private Buyer'],
                     title='Pie chart of user distribution in all nations of the continent Faerun')
        fig.update_layout(width=400, height=300)
        return fig
    else:
        x_corr = clickData['points'][0]['x']
        filtered_df = df[df['x'] == x_corr]
        nation = filtered_df.iloc[0]['Nation']
        values=[filtered_df.iloc[0]['Key Account'],
                             filtered_df.iloc[0]['No Key Account'],
                             filtered_df.iloc[0]['Private Buyer']
                             ]
        fig = px.pie(values=values, 
                     names=['Key Account','No Key Account','Private Buyer'], title=f'Pie chart of user distribution in Nation {nation}')
        fig.update_layout(width=400, height=300)
        return fig

# callback function of products subtypes bar chart
@callback(
    Output('details-graph-products-bar-chart', 'figure'),
    Input('map-graph', 'clickData')
)
def update_details(clickData):
    if clickData is None:
        subtype_count_sum = subtype_count.drop('Nation',axis=1)
        subtype_count_sum.loc['Sum'] = subtype_count_sum.sum()
        subtype_count_sum_ordered = subtype_count_sum.loc['Sum'].sort_values()
        fig = px.bar(subtype_count_sum_ordered, title='Sales by Subtype of all nations',orientation='h')
        fig.update_layout(width=1000, height=800)
        return fig
    else:
        x_corr = clickData['points'][0]['x']
        filtered_df = df[df['x'] == x_corr]
        nation = filtered_df.iloc[0]['Nation']
        subtype_df = subtype_count[subtype_count['Nation'] == nation]
        subtype_df_transposed = subtype_df.T
        subtype_df_transposed.columns= subtype_df_transposed.loc['Nation']
        subtype_df_transposed  = subtype_df_transposed.drop('Nation')
        subtype_df_ordered=subtype_df_transposed.sort_values(by=nation, ascending=True)
        fig = px.bar(x=subtype_df_ordered[nation], y=subtype_df_ordered.index, title='Sales by Subtype',orientation='h')
        fig.update_layout(width=1000, height=800)
        return fig


# callback function of territory suborders bar chart
@callback(
    Output('details-graph-territory-bar-chart', 'figure'),
    Input('map-graph', 'clickData')
)
def update_details(clickData):
    if clickData is None:
        nation = 'Aglarond'
        Sub_orders = sub_orders[sub_orders['Nation'] == nation]
        Sub_orders_ordered = Sub_orders.sort_values(by='territory_ordersCount', ascending=False)
        fig = px.bar(x=Sub_orders_ordered['Territory'],y=Sub_orders_ordered['territory_ordersCount'],
                     title=f'An example of orders in each territory within Nation {nation}')
        fig.update_layout(width=600, height=300)
        return fig
    else:
        x_corr = clickData['points'][0]['x']
        filtered_df = df[df['x'] == x_corr]
        nation = filtered_df.iloc[0]['Nation']
        Sub_orders = sub_orders[sub_orders['Nation'] == nation]
        Sub_orders_ordered = Sub_orders.sort_values(by='territory_ordersCount', ascending=False)
        fig = px.bar(x=Sub_orders_ordered['Territory'],y=Sub_orders_ordered['territory_ordersCount'],
                     title=f'Bar chart of orders in each territory of Nation {nation}')
        fig.update_layout(width=600, height=300)
        return fig


# callback function of dropdown

@callback(
    Output('map-graph', 'figure'),
    [Input('option-dropdown', 'value')]
)
def update_figure(selected_option):
    fig = go.Figure()
    # Add an image as the map background
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=gray_image_path
            )
    )
    # set chart layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        xaxis=dict(showgrid=False, zeroline=False, range=[0, img_width * scale_factor]),
        yaxis=dict(showgrid=False, zeroline=False, range=[0, img_height * scale_factor]),
        plot_bgcolor='rgba(0,0,0,0)',
        clickmode='event+select'
    )
    for index, row in df.iterrows():
        if selected_option == 'Total orders':
            fig.add_trace(go.Scatter(x=[row['x']], y=[row['y']],
                             text=row['Nation'],
                             name=row['Nation'],
                             mode='markers',
                             hovertext='orders: '+str(row['Total_orders']),
                             marker=dict(
                                 size=row['Total_orders']/100,
                                 sizemode='area',
                                 sizeref=row['Total_orders']/1000,
                                 sizemin=10,
                                 color=[row['Total_orders']/100],  # set the color of the point
                                 colorscale='Viridis',  # color mapping scheme
                                 opacity=0.8,
                                 cmin=1,
                                 cmax=175,
                                 line_color='rgb(40,40,40)',
                                 line_width=0.5,
                                 colorbar=dict(title='Orders(/100)',x=1.3,y=0.5,
                                               thickness=20,  # adjust the width of the color bar
                                               len=0.75,  # adjust the length of the color bar
                                               title_font=dict(size=12),  # adjust the title font size
                                               tickfont=dict(size=10),
                                               tickvals=[1,50,100,150])
                                               #ticktext=['Low', 'Medium', 'High'])
                             )))
                             #textposition="top center"))
        elif selected_option == 'Total customers':
            fig.add_trace(go.Scatter(x=[row['x']], y=[row['y']],
                             text=row['Nation'],
                             name=row['Nation'],
                             mode='markers',
                             hovertext='customers: '+str(row['Total_customers']),
                             marker=dict(
                                 size=row['Total_customers'],
                                 sizemode='area',
                                 sizeref=row['Total_customers'],
                                 sizemin=10,
                                 color=[row['Total_customers']],  # set the color of the point
                                 colorscale='Viridis',  # color mapping scheme
                                 opacity=0.8,
                                 cmin=1,
                                 cmax=175,
                                 line_color='rgb(40,40,40)',
                                 line_width=0.5,
                                 colorbar=dict(title='Customers',x=1.3,y=0.5,
                                               thickness=20,  # adjust the width of the color bar
                                               len=0.75,  # adjust the length of the color bar
                                               title_font=dict(size=12),  # adjust the title font size
                                               tickfont=dict(size=10),
                                               tickvals=[1,50,100,150])
                                               #ticktext=['Low', 'Medium', 'High'])
                             )))
        else:
            fig.add_trace(go.Scatter(x=[row['x']], y=[row['y']],
                             #text=row['Nation'],
                             name=row['Nation'],
                             mode='markers+text',
                             hovertext='Cart Price (In CP): '+str(row['Total_CartPrice']),
                             marker=dict(
                                 size=row['Total_CartPrice']/1000000,
                                 sizemode='area',
                                 sizeref=row['Total_CartPrice']/1000000,
                                 sizemin=10,
                                 color=[row['Total_CartPrice']/1000000],  # set the color of the point
                                 colorscale='Viridis',  # color mapping scheme
                                 opacity=0.8,
                                 cmin=1,
                                 cmax=175,
                                 line_color='rgb(40,40,40)',
                                 line_width=0.5,
                                 colorbar=dict(title='Cart Price (In CP)(/10e6)',x=1.3,y=0.5,
                                               thickness=20,  # adjust the width of the color bar
                                               len=0.75,  # adjust the length of the color bar
                                               title_font=dict(size=12),  # adjust the title font size
                                               tickfont=dict(size=10),
                                               tickvals=[1,50,100,150])
                                               #ticktext=['Low', 'Medium', 'High'])
                             )))
    return fig
