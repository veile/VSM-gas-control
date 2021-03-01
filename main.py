from collections import deque
from datetime import datetime

from dash.dependencies import Output, Input

from app import app, colors
from app.mks import MFC

import dash_html_components as html
import app.components as comp

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots


H2_ADDR = 252
AR_ADDR = 253

YH2 = deque([MFC().read_flow(H2_ADDR)], maxlen=100)
YAr = deque([MFC().read_flow(AR_ADDR)], maxlen=100)

#T = deque(datetime.now(tz=None).strftime("%Y-%m-%d %H:%M:%S"), maxlen=100)
T = deque([1], maxlen=100)

# Main Page layout
index_page = html.Div(
    style={
        'backgroundColor': colors['background']
    },
    children=[
        comp.markdown('# Gas Flow Control - In-situ VSM', plc='center'),
        comp.ar_div(),
        comp.h2_div(),
        comp.graph()
    ]
)

app.layout = index_page

# Callbacks
@app.callback(
    Output('flow_graph', 'figure'),
    Input('flow_interval', 'n_intervals')
)
def update_flow_graph(n):
    YAr.append(MFC().read_flow(AR_ADDR))
    YH2.append(MFC().read_flow(H2_ADDR))

    #T.append(datetime.now(tz=None).strftime("%H:%M"))
    T.append(n)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=list(T), y=list(YAr), name="Argon flow"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=list(T), y=list(YH2), name="Hydrogen flow"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Measured flow"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")

    # Set y-axes titles
    fig.update_yaxes(
        title_text="Argon flow",
        secondary_y=False)
    fig.update_yaxes(
        title_text="Hydrogen flow",
        secondary_y=True)

    return fig


@app.callback(
    Output('ar_submit_text', 'children'),
    [Input('ar_set_flow_submit', 'n_clicks'),
     Input('ar_set_flow', 'n_submit'),
     Input('ar_set_flow', 'value')]
)
def set_flow_ar(nc, ne, f):
    if nc is None and ne is None:
        sx = MFC().comm('SX?', AR_ADDR)
        return "Current setpoint: %s" %sx

    MFC().set_flow(f, AR_ADDR)

    sx = MFC().comm('SX?', AR_ADDR)
    return "Current setpoint: %s" %sx

@app.callback(
    Output('h2_submit_text', 'children'),
    [Input('h2_set_flow_submit', 'n_clicks'),
     Input('h2_set_flow', 'n_submit'),
     Input('h2_set_flow', 'value')]
)
def set_flow_h2(nc, ne, f):
    if nc is None and ne is None:
        sx = MFC().comm('SX?', H2_ADDR)
        return "Current setpoint: %s" %sx

    MFC().set_flow(f, H2_ADDR)

    sx = MFC().comm('SX?', H2_ADDR)
    return "Current setpoint: %s" %sx


if __name__ == '__main__':
        app.run_server(debug=True, host='0.0.0.0')
