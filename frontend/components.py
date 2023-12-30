import dash_bootstrap_components as dbc
from dash import dcc, html

client_mem = dcc.Store(id="client-mem", storage_type="session", data={})

initial_conditions_btn = dbc.Button(
    id="ic-btn", children="New Initial Conditions", n_clicks=0
)
initial_conditions_inputs = html.Div(
    [
        dbc.Input(id=f"ic-input-{i}", type="number", placeholder=val, value=0)
        for i, val in enumerate(["x0", "y0", "a", "b", "c", "d", "e", "f"])
    ]
)

function_dropdown = dcc.Dropdown(
    id="function-dropdown",
    options=[
        {"label": "Clifford", "value": "Clifford"},
        {"label": "De Jong", "value": "de_jong"},
        {"label": "Bedhead", "value": "bedhead"},
    ],
    value="Clifford",
)

make_gif_btn = dbc.Button(id="make-gif-btn", children="Make Gif", n_clicks=0)

output_gif_div = html.Div(id="output-gif-div", children="")

layout = html.Div(
    [
        client_mem,
        html.H1("My Dash App"),
        initial_conditions_btn,
        initial_conditions_inputs,
        function_dropdown,
        make_gif_btn,
        output_gif_div,
    ]
)
