import base64

import requests
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from loguru import logger

from src.client_mem_model import ClientMemModel
from src.settings import settings

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
"""
# layout = html.Div([
#     #,style={'width': '80vh', 'height': '80vh'}),
#     dbc.Container([
#         dbc.Row([
#             dbc.Col(html.H5(
#              children=["Welcome, please wait for your attractor to generate before clicking the",
#                        ' button or dropdown if one doesnt generate in 30 second you may try clicking',
#                        ' the button this page is a work in progress!',
#                        html.Br(),
#                        ' The base code is from ',
#     html.A("Lázaro Alonso",href='https://lazarusa.github.io/Webpage/index.html'),
#     ' I didnt see any place for less technical people to generate and',
#     ' color there own attractors and wanted to share with my sisters and friends'], className="text-center")
#                     , className="mb-5 mt-5")
#         ]),
#      ]),
#     html.Div([
#             html.Img(id='frac',)
#     ], style={'textAlign': 'center'}),


#     dbc.Row([
#             dbc.Col(html.H6(
#              children=[
#               #http://www.pickover.com/
# html.A("This program uses Cliff Pickover's formula",href="http://www.pickover.com/"),
# html.Br(),
#     'x = sin(a * y) + c * np.cos(a * x)',html.Br(),
#     'y = np.sin(b * x) + d * np.cos(b * y)',html.Br(),

#    ' Fractals work by you starting with some initial conditions.
 I start with x[0] and y[0] = 0 and 4 other set parameters a,b,c, and d.'
#    ' Then with the initial conditions and the other 4 parameter the values are put into the clifford equation.'
#    ' It will give you a new x[1] and y[1] value as a result.'
#    ' Then feed that result into the equation again to get a new result x[3] & y[3].'
#    ' Then you do that again and again putting you previous result into the equation.'
#    ' The fractals you see here are run through this equation 100,000,000 times.'
#    ' The images is colored based on how many times the the result landed in a certain pixel value',html.Br(),
#    ' Not all of these initial conditions generate "interesting" ',
#               " or chaotic works actually most don't",
#    ' I bit of extra math to find parameters that generate what I think are more interesting/pretty fractals. '
#    ' I also do some fancy math to compute them more efficiently.'
#    ' As they are easy to calculate but become very spacious and slow to calculate very fast.'
#    ' Too big and slow for Heroku who im using to host this site and turn it into
a google cloud serverless api function call.',html.Br(),
#
#    ' I want people to be able to generate and color there own fractals and admire',
#    ' their beauty as I do with every one.'

#              ])
#                     , className="mb-5 mt-5")
#         ]),

# ])
"""


def register_callbacks(app):  # noqa: C901
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
            url = settings.backend_url / "api/attractors/initial-conditions"

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
        Output("make-gif-btn", "disabled"),
        Input("make-gif-btn", "n_clicks"),
        State("function-dropdown", "value"),
        State("color-dropdown", "value"),
        State("client-mem", "data"),
    )
    def update_output_div(n_clicks, function_val, color_map_val, client_mem_dict):
        if n_clicks == 0 or n_clicks is None:
            raise PreventUpdate
        else:
            client_mem = ClientMemModel(**client_mem_dict)
            post_data = {
                "initial_conditions": client_mem.initial_conditions,
                "function": function_val,
                "color_map": color_map_val,
            }
            logger.debug(f"Making gif post_data: {post_data}")
            url = settings.backend_url / "api/attractors/make-gif"
            response = requests.post(url, json=post_data)
            if response.status_code == 200:
                # Request was successful
                gif_data = base64.b64encode(response.content).decode()
                gif_data_url = f"data:image/gif;base64,{gif_data}"
                return html.Img(src=gif_data_url, className="responsive-img"), False

            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                return (
                    html.Div(children=f"Request failed {response.status_code}"),
                    False,
                )
