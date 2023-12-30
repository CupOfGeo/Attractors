"""
user flow

connects to site a default attractor is rendered

sliders for initial conditions
button for new initial conditions

maybe its a two page app design the frac then design the gif
things you can do with the gif

length of the gif
number of frames in the gif == how many points get added per frame
this is the np.geospace
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from frontend.client_mem_model import ClientMemModel

app = dash.Dash(__name__, suppress_callback_exceptions=True)

client_mem = dcc.Store(
    id="client-mem", storage_type="session", data=ClientMemModel([0, 0, 0, 0, 0, 0])
)

initial_conditions_btn = dbc.Button(
    id="ic-btn", children="New Initial Conditions", n_clicks=0
)
initial_conditions_inputs = html.Div(
    [
        dbc.Input(id=f"ic-input-{i}", type="number", placeholder=val, value=0)
        for i, val in enumerate(["x0", "y0", "a", "b", "c", "d"])
    ]
)

function_dropdown = dcc.Dropdown(
    id="function-dropdown",
    options=[
        {"label": "Clifford", "value": "clifford"},
        {"label": "De Jong", "value": "de_jong"},
        {"label": "Bedhead", "value": "bedhead"},
    ],
    value="clifford",
)
output_gif_div = html.Div(id="output-gif-div", children="")

app.layout = html.Div(
    [
        html.H1("My Dash App"),
        initial_conditions_btn,
        initial_conditions_inputs,
        function_dropdown,
        output_gif_div,
    ]
)


@app.callback(
    Output("client-mem", "data"),
    Input("ic-btn", "n_clicks"),
)
def update_client_mem(n_clicks):
    if n_clicks == 0 or None:
        raise PreventUpdate
    else:
        return ClientMemModel([1, 2, 3, 4, 5, 6])


@app.callback(
    [
        Output("ic-input-0", "value"),
        Output("ic-input-1", "value"),
        Output("ic-input-2", "value"),
        Output("ic-input-3", "value"),
        Output("ic-input-4", "value"),
        Output("ic-input-5", "value"),
    ],
    Input("client-mem", "data"),
)
def update_initial_conditions(client_mem):
    if client_mem is None:
        raise PreventUpdate
    else:
        return (
            client_mem.initial_conditions[0],
            client_mem.initial_conditions[1],
            client_mem.initial_conditions[2],
            client_mem.initial_conditions[3],
            client_mem.initial_conditions[4],
            client_mem.initial_conditions[5],
        )


@app.callback(
    Output("output-gif-div", "children"), [Input("initial-conditions-btn", "n_clicks")]
)
def update_output_div(n_clicks):
    if n_clicks == 0:
        return html.Div(id="output-gif-div", children="")
    else:
        return html.Div(id="output-gif-div", children="New Initial Conditions Clicked")


if __name__ == "__main__":
    app.run_server(debug=True)
