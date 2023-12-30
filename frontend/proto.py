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
import base64

import dash
import requests
from client_mem_model import ClientMemModel
from components import layout
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger

app = dash.Dash(__name__, suppress_callback_exceptions=False)

app.layout = layout


@app.callback(
    Output("ic-input-0", "value"),
    Output("ic-input-1", "value"),
    Output("ic-input-2", "value"),
    Output("ic-input-3", "value"),
    Output("ic-input-4", "value"),
    Output("ic-input-5", "value"),
    Output("ic-input-6", "value"),
    Output("ic-input-7", "value"),
    Input("ic-btn", "n_clicks"),
    State("function-dropdown", "value"),
)
def update_client_mem(n_clicks, function_val):
    logger.debug(f"n_clicks: {n_clicks}, function_val: {function_val}")
    if n_clicks == 0 or None:
        raise PreventUpdate
    else:
        logger.debug("Updating client memory [12345]")
        url = "https://attractors-service-c6dyl3tniq-uc.a.run.app/api/attractors/initial-conditions"

        response = requests.post(
            url, json={"function": function_val, "percent_empty": 0}
        )
        if response.status_code == 200:
            # Request was successful
            logger.debug(response.text)
            ic_list = response.json()
            return tuple(ic_list)
        else:
            # Request failed
            logger.error(f"Request failed with status code: {response.status_code}")
            # todo return an error to the user maybe a toast that says failed
            # would requirer an extra fail output toast
            return tuple(["error", 2, 3, 4, 5, 6, 7, 8])


@app.callback(
    Output("client-mem", "data"),
    Input("ic-input-0", "value"),
    Input("ic-input-1", "value"),
    Input("ic-input-2", "value"),
    Input("ic-input-3", "value"),
    Input("ic-input-4", "value"),
    Input("ic-input-5", "value"),
    Input("ic-input-6", "value"),
    Input("ic-input-7", "value"),
)
def update_initial_conditions(v0, v1, v2, v3, v4, v5, v6, v7):
    ic_list = [v0, v1, v2, v3, v4, v5, v6, v7]
    logger.debug(f"ICs: {ic_list}")
    if all(v is None or v == 0 for v in ic_list):
        raise PreventUpdate
    else:
        logger.debug("Updating client memory with ICs")
        return ClientMemModel(ic_list).to_dict()


@app.callback(
    Output("output-gif-div", "children"),
    Input("make-gif-btn", "n_clicks"),
    State("function-dropdown", "value"),
    State("client-mem", "data"),
)
def update_output_div(n_clicks, function_val, client_mem_dict):
    if n_clicks == 0 or n_clicks is None:
        raise PreventUpdate
    else:
        client_mem = ClientMemModel(**client_mem_dict)
        post_data = {
            "initial_conditions": client_mem.initial_conditions,
            "function": function_val,
            "color_map": "fire",
        }
        logger.debug(f"Making gif post_data: {post_data}")
        url = (
            "https://attractors-service-c6dyl3tniq-uc.a.run.app/api/attractors/make-gif"
        )
        response = requests.post(url, json=post_data)
        if response.status_code == 200:
            # Request was successful
            gif_data = base64.b64encode(response.content).decode()
            gif_data_url = f"data:image/gif;base64,{gif_data}"
            return html.Img(src=gif_data_url)

        else:
            logger.error(f"Request failed with status code: {response.status_code}")
            return html.Div(children=f"Request failed {response.status_code}")


if __name__ == "__main__":
    app.run_server(debug=True)
