import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/',
                   title="Home page",
                   name='Home page',
                   order=0)


layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H3(children="Welcome!")
        ])
    ]),
    dbc.Row([
        html.Div([
            html.P(children="In this APP, you can explore D.E.A.D dataset.",className="mb-0"),
            html.P(children="Please click on the left column (content), to play with data visualization.",className="mb-0"),
            html.Br(),
            html.H3(children="General Information"),
            html.Div("Click on the each section below for detailed description"),
            html.Div([
                dbc.Accordion([
                    dbc.AccordionItem(
                        [
                            html.P(children="To explore the relationship between 'where' and 'what' "),
                            html.P(children="Based on this page of visualization, you will be able to have insights about which nation holds the most orders/customers/cart price, which subtypes of products have the best sales in that nation and what are their main customers with the distribution of the 3 main customer types.")
                        ],
                        title="Visualization plot 1",
                    ),
                    dbc.AccordionItem([
                        html.P(children="To explore the relationship between 'when' and 'what' "),
                        html.P(children="..."),
                    ],
                        title="Visualization plot 2"),
                ],
                always_open=True,
                flush=True,style={"width":"11cm"})
            ]),
    ]),

]),
    html.Br(),
    html.Br(),
    dbc.Row([
        html.Div([
            html.H3(children="Team Member:"),
            html.Div('Fan Yu (r0862624)'),
            html.Div('John Kyle Cooper (r0877058)'),
            html.Div('Yu-Ting, Ma(r0957353)')
        ])
    ])
])
