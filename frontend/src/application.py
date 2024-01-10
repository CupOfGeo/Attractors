import dash_bootstrap_components as dbc
import src.frontend as frontend
from dash import Dash, html
from src.backend_check import backend_check, backend_check_layout
from src.components import layout


def get_app():
    """
    Get dash application.
    """
    app = Dash(
        name="Attractors",
        assets_folder="src/assets",
        # if generating components dynamically, set this to True if your getting an error
        suppress_callback_exceptions=False,
        external_stylesheets=[dbc.themes.LUX],
        title="Attractors",
        update_title="Loading...",
    )
    # configure_logging()
    backend_check(app)
    frontend.register_callbacks(app)
    app.layout = html.Div([backend_check_layout, layout])
    return app.server
