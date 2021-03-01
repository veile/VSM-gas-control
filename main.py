from dash.dependencies import Output, Input


from app import app, colors
from app.mks import MFC

import dash_html_components as html
import app.components as comp

import plotly
import plotly.graph_objs as go

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

Y = [MFC().read_flow(253)]
# Y = [1]

# Callbacks
@app.callback(
    Output('flow_graph', 'figure'),
    Input('flow_interval', 'n_intervals')
)
def update_flow_graph(n):
    Y.append(MFC().read_flow(253))
    
    X = [i for i in range(len(Y))]

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]), yaxis=dict(range=[min(Y), max(Y)]), )}


@app.callback(
    Output('ar_submit_text', 'children'),
    [Input('ar_set_flow_submit', 'n_clicks'),
     Input('ar_set_flow', 'n_submit'),
     Input('ar_set_flow', 'value')]
)
def set_flow_ar(nc, ne, f):
    if nc is None and ne is None:
        return ""

    MFC().set_flow(f, 253)

    sx = MFC().comm('SX?', 253)
    return "Set Point set to %s" %sx
    # return "Set Point set to %.2f" %f


if __name__ == '__main__':
        app.run_server(debug=True, host='0.0.0.0')