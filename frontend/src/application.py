import dash_bootstrap_components as dbc
from dash import Dash

from src.components import layout
from src.logging import configure_logging


def get_app() -> Dash:
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
    configure_logging()
    app.layout = layout

    return app
