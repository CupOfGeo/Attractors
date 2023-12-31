import requests
from dash import dcc, html
from dash.dependencies import Input, Output
from loguru import logger

from src.settings import settings

backend_check_layout = html.Div(
    [
        html.Div(
            id="circle",
            children=html.Div(
                style={
                    "width": "100px",
                    "height": "100px",
                    "background-color": "yellow",
                    "border-radius": "50%",
                }
            ),
        ),
        dcc.Interval(id="interval", interval=1000 * 60),
    ]
)


def backend_check(app):
    @app.callback(Output("circle", "children"), [Input("interval", "n_intervals")])
    def update_circle(n):
        logger.debug(
            f"Checking backend health {str(settings.backend_url)} /manage/health"
        )
        response = requests.get(settings.backend_url / "manage/health")
        if response.status_code == 200:
            logger.debug("Backend is healthy")
            color = "green"
        else:
            logger.error("Backend is not healthy")
            color = "red"
        return html.Div(
            style={
                "width": "100px",
                "height": "100px",
                "background-color": color,
                "border-radius": "50%",
            }
        )
