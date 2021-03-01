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
 
# Callbacks
@app.callback(
    Output('flow_graph', 'figure'),
    Input('flow_interval', 'n_intervals')
)
def update_flow_graph(n):
    if n == 0:
      pass
      

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


if __name__ == '__main__':
        app.run_server(debug=True, host='0.0.0.0')