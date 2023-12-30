import requests
from dash import dcc, html
from dash.dependencies import Input, Output

from settings import settings

backend_check_layout = [
    html.Div(id="circle"),
    dcc.Interval(id="interval", interval=1000 * 30, n_intervals=0),
]


def backend_check(app: dash.Dash):
    @app.callback(Output("circle", "children"), [Input("interval", "n_intervals")])
    def update_circle(n):
        response = requests.get(settings.backend_url + "/manage/health")
        if response.status_code == 200:
            color = "green"
        else:
            color = "red"
        return html.Div(
            style={
                "width": "100px",
                "height": "100px",
                "background-color": color,
                "border-radius": "50%",
            }
        )
