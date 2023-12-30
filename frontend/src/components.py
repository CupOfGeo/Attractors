import dash_bootstrap_components as dbc
from dash import dcc, html

client_mem = dcc.Store(id="client-mem", storage_type="session", data={})

initial_conditions_btn = dbc.Button(
    id="ic-btn", children="New Initial Conditions", className="m-1", n_clicks=0
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

cmap_dropdown = dcc.Dropdown(
    id="color-dropdown",
    options=[
        {"label": "Inferno", "value": "inferno"},
        {"label": "Virdis", "value": "viridis"},
    ],
    value="inferno",
)

make_gif_btn = dbc.Button(
    id="make-gif-btn", children="Make Gif", className="m-1", n_clicks=0
)

loading_gif_btn = dcc.Loading(id="loading-gif", type="circle", children=make_gif_btn)

output_gif_div = html.Div(id="output-gif-div", children="")

layout = html.Div(
    [
        client_mem,
        html.H1("My Dash App"),
        initial_conditions_btn,
        initial_conditions_inputs,
        function_dropdown,
        cmap_dropdown,
        loading_gif_btn,
        output_gif_div,
    ]
)
