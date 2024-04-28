import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

image_path = "https://raw.githubusercontent.com/AgnesLigh/Data_Visualization_D.E.A.D/main/map.png"
image_url = image_path
background_image=html.Img(image_url)

fig = go.Figure()

# Constants
img_width = 1600
img_height = 900
scale_factor = 0.7

# Dash Application Layout
app.layout = html.Div([
    dcc.Graph(id='map-graph', figure=fig),
    html.Div(id='selected-data', children=[
        dcc.Graph(id='detail-graph')
    ]) #, backgroud_image
])

# Adds a callback to handle point-click events
@app.callback(
    Output('detail-graph', 'figure'),
    Input('map-graph', 'clickData'))
def display_click_data(clickData):
    if clickData is None:
        fig_none=go.Figure()
        fig_none.update_layout(width=400, height=300, title_text="Simple Pie Chart Example")

        return fig_none
    else:
        # Extract the click point information and display it
        point_index = clickData['points'][0]['pointIndex']
        All=custom_points[point_index]["Normal users"]
        Key=custom_points[point_index]["Key users"]
        fig_detail=go.Figure(go.Pie(values=[All, Key], labels=["Normal users", "Key users"]))
        fig_detail.update_layout(width=400, height=300, title_text="Simple Pie Chart Example")
        return fig_detail


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
        source=image_path
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


# Add fictive points
custom_points = [
    {"name": "Baldur's Gate", "x": 254, "y": 396, "order": 100, "Normal users": 900, "Key users":800},
    {"name": "Amn", "x": 320, "y": 329, "order": 1000, "Normal users": 1070, "Key users":300},
    {"name": "Aglarond", "x": 755, "y": 413, "order": 200, "Normal users": 1060, "Key users":550},
    {"name": "Calimshan", "x": 345, "y": 187, "order": 300, "Normal users": 900, "Key users":300},
    {"name": "Chessentea", "x": 770, "y": 320, "order": 400, "Normal users": 700, "Key users":400},
    {"name": "Chondath", "x": 650, "y": 300, "order": 700, "Normal users": 1100, "Key users":300},
    {"name": "Cormyr", "x": 465, "y": 433, "order": 600, "Normal users": 800, "Key users":470},
    {"name": "Damara", "x": 685, "y": 565, "order": 1100, "Normal users": 1700, "Key users":400},
    {"name": "Dambrath", "x": 810, "y": 76, "order": 800, "Normal users": 1200, "Key users":500}
]

for point in custom_points:
    fig.add_trace(go.Scatter(x=[point['x']], y=[point['y']],
                             mode='markers+text',
                             marker=dict(
                                 size=point['order']/10,
                                 sizemode='area',
                                 sizeref=point['order']/1000,
                                 sizemin=10,
                                 color=[point['order']/100],  # set the color of the point
                                 colorscale='Viridis',  # color mapping scheme
                                 opacity=0.7,
                                 cmin=1,
                                 cmax=15,
                                 colorbar=dict(title='Orders',x=1.3,y=0.5,
                                               thickness=20,  # adjust the width of the color bar
                                               len=0.75,  # adjust the length of the color bar
                                               title_font=dict(size=12),  # adjust the title font size
                                               tickfont=dict(size=10),
                                               tickvals=[1,10,15])
                                               #ticktext=['Low', 'Medium', 'High'])
                             ),
                             name=point['name'],
                             text='orders: '+str(point['order']),
                             textposition="top center"))


if __name__ == '__main__':
    app.run_server(debug=True)