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
data = {
    'Date': pd.date_range(start='2021-01-01', periods=100, freq='D'),
    'Sales': np.random.randint(100, 500, size=100)  # 随机生成销售数据
}
df = pd.DataFrame(data)


layout= dbc.Container([
  dbc.Row([
        html.Div([
            html.H3(children="To explore the relationship between 'when' and 'what' "),
            html.P("This plot aims to find possible relationship between ...")
        ], style={"width":"20cm"})
    ]),
    html.Br(),
    html.Div([
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='sales-bar-chart')
])
])

@callback(
    Output('sales-bar-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    # 根据日期过滤数据
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df.loc[mask]
    
    # 使用Plotly创建柱状图
    fig = px.bar(filtered_df, x='Date', y='Sales', title='Sales by Date')
    return fig
