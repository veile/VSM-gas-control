import dash
import dash_auth
from flask import Flask, send_from_directory

VALID_USERNAME_PASSWORD_PAIRS = {
    'MKS FC': 'mag1234'
}

mathjax = ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/static/reset.css']
# stylesheets = ['/static/style.css']
app = dash.Dash(__name__)#, external_stylesheets=stylesheets, external_scripts=mathjax)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

colors = {
    'background': '#F9F9F9',
    'text': '#7FDBFF',
}