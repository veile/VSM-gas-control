from app import colors

import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html

def markdown(text, plc='center'):
    return dcc.Markdown(children=text,
                        style={
                            'textAlign' : plc
                        }
    )

def ar_div():
    return html.Div(
        style=
        {'width' : '20%',
               'height': 270,
               'padding': '20px',
               'marginRight': 5,
               'float': 'left',
               'backgroundColor': colors['background'],
               'borderStyle': 'solid',
               'borderColor': '#616161'
        },
        children=
        [
            html.Label("Argon flow"),
            html.Br(),
            dcc.Input(
                id='ar_set_flow',
                persistence=False,
                type = 'number'
            ),
            html.Br(),
            html.Button("Submit", id='ar_set_flow_submit'),
            html.Div(id='ar_submit_text')
        ],
        id='ar_div'
    )

def h2_div():
    return html.Div(
        style=
        {'width' : '20%',
               'height': 270,
               'padding': '20px',
               'marginRight': 5,
               'float': 'left',
               'backgroundColor': colors['background'],
               'borderStyle': 'solid',
               'borderColor': '#616161'
        },
        children=
        [
            html.Label("Hydrogen flow"),
            html.Br(),
            dcc.Input(
                id='h2_set_flow',
                persistence=False,
                type = 'number'
            ),
            html.Br(),
            html.Button("Submit", id='h2_set_flow_submit'),
            html.Div(id='h2_submit_text')
        ],
        id='h2_div'
    )

def graph():
    return html.Div(
        style=
        {'width' : '60%',
               'height': 270,
               'padding': '20px',
               'marginRight': 5,
               'float': 'left',
        },
        children=
        [
            dcc.Interval(id='flow_interval', interval=5000, n_intervals=0),
            dcc.Graph(id='flow_graph', animate=True)
        ],
        id='graph_div'
    )