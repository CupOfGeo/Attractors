# import json
# import random

# import dash_bootstrap_components as dbc
# import numpy as np
# import pandas as pd
# from dash import dcc, html
# from dash.dependencies import Input, Output
# from PIL import Image

# # have have a buffer of a images so you don't wait as long
# # (still make them wait a few seconds for the illusion of computing)

# init_list = [[0.0,
#   0.0,
#   -1.6638516812438717,
#   1.5181966416940011,
#   -0.7363844485273741,
#   -0.8408412108307393,
#   -0.4766741805112438,
#   -1.866394436977353],
#  [0.0,
#   0.0,
#   1.741392789646223,
#   -1.9346049895634891,
#   0.9707774588150473,
#   -0.7638781190700161,
#   0.3628363678711679,
#   1.268400054537564],
#  [0.0,
#   0.0,
#   -1.498019400082332,
#   -1.5108441347904447,
#   0.9629820923645562,
#   0.09765815688636881,
#   0.34435879288500715,
#   1.575738558730893],
#  [0.0,
#   0.0,
#   -1.5089596688432239,
#   1.1982434877652017,
#   -1.263497810005335,
#   1.6702487996517976,
#   1.2401058959224622,
#   -1.2477945651291495],
#  [0.0,
#   0.0,
#   -1.2988289283918135,
#   1.6953210866064765,
#   -1.742865879133927,
#   1.637471737592219,
#   0.6635925586440008,
#   -1.2657612127849331],
#  [0.0,
#   0.0,
#   1.7275595435443605,
#   -1.9116500306108715,
#   -1.741503380267741,
#   -1.8528167101412882,
#   0.0699360208665607,
#   0.6808143279342644],
#  [0.0,
#   0.0,
#   -1.1348161793507394,
#   -1.9965097908247564,
#   1.3963808104372917,
#   -0.6527769249016946,
#   -0.7403532495815361,
#   1.6848415838597783],
#  [0.0,
#   0.0,
#   -1.3675569778093557,
#   -1.8575636369443078,
#   0.14765146604265045,
#   -1.9988375941866083,
#   -0.8058048507819668,
#   -0.11282683099236257],
#  [0.0,
#   0.0,
#   -1.7510491712350742,
#   1.9330027747857637,
#   1.199749894253694,
#   1.181633772759981,
#   1.3223741579830457,
#   0.5691924570804243],
#  [0.0,
#   0.0,
#   -1.6291820195414775,
#   1.5926522681414128,
#   0.8581480683467015,
#   1.2920933863678261,
#   0.06847144079082446,
#   -1.7791819270592932],
#  [0.0,
#   0.0,
#   1.1771020471329416,
#   -1.4950880215632343,
#   1.7641330258127224,
#   1.0328525833482067,
#   -0.40398041296564813,
#   -0.5612183038867133],
#  [0.0,
#   0.0,
#   1.9034333472752532,
#   -1.95038921068247,
#   -0.9360757099647228,
#   1.9156171273177134,
#   0.02195871813382899,
#   -1.9771951192517254],
#  [0.0,
#   0.0,
#   1.755285498079957,
#   -1.8917816549718522,
#   -0.7400782745164864,
#   -1.2642315222632243,
#   0.7853249648869012,
#   0.9897207612229608],
#  [0.0,
#   0.0,
#   1.7333339351306045,
#   -0.5577834319757922,
#   1.8892743686417304,
#   0.21743082962441385,
#   1.6077306077123414,
#   -1.8108571643120617],
#  [0.0,
#   0.0,
#   0.8807573973381801,
#   1.7749810312439593,
#   -1.6269824575111667,
#   -1.3008664984213105,
#   -0.9986760368623395,
#   1.4704352306081634],
#  [0.0,
#   0.0,
#   1.4402979057329763,
#   -0.577134827433238,
#   1.8560953852462476,
#   0.5953078974501693,
#   0.7353505443404957,
#   -1.9284909665592567],
#  [0.0,
#   0.0,
#   1.4689661937588223,
#   1.208085102889663,
#   -1.3300814715656863,
#   -1.1263384809098036,
#   1.0990505303666098,
#   1.406111605146831],
#  [0.0,
#   0.0,
#   -1.0605404219670826,
#   1.9788781168695855,
#   -1.6068918569288093,
#   -0.5084751320792957,
#   -0.8357998735692904,
#   0.884192270663561],
#  [0.0,
#   0.0,
#   1.5108602864282705,
#   -1.5824982602391588,
#   1.7347837812311062,
#   -0.5504868737353212,
#   -1.6048842886098433,
#   -1.3040784361025493]]


# big_cmaps = [
#  #'CET_C5',
#  'CET_C1s',
#  'CET_C2',
#  'colorwheel',
#  #'CET_CBC1',
#  #'CET_CBC2',
#  #'CET_CBTC1',
#  #'CET_CBTC2',
#  #'CET_C4',
#  'CET_C4s',
#  'bkr', #nice
#  'bky',
#  'CET_D13',
#  'CET_D1A',
#  'coolwarm',
#  'CET_D9',
#  'CET_D10',
#  'diverging_gkr_60_10_c40',
#  'CET_D3',
#  'gwv',
#  #'CET_D12',
#  'diverging_isoluminant_cjm_75_c24',
#  'CET_D11',
#  'CET_D8',
#  'bjy',
#  #'bwy',
#  'CET_R3',
#  #'cwr',
#  'CET_I1',
#  #'isolum', #lighter version of above
#  'CET_I3',
#  'bgy', #NOICE
#  'linear_bgyw_15_100_c67',
#  'bgyw',
#  'CET_L9',
#  'kbc',
#  'blues',
#  'CET_L7',
#  'bmw',
#  'CET_L8',
#  'bmy',
#  #'CET_L10',
#  #'CET_L11',
#  'kgy',
#  'gray',
#  'dimgray',
#  'CET_L16',
#  'kgy',
#  'CET_L4',
#  'linear_kry_5_95_c72',
#  'linear_kry_5_98_c75',
#  'fire',
#  'linear_kryw_5_100_c64',
#  'linear_kryw_5_100_c67',
#  'CET_CBL1',
#  'CET_CBL2',
#  'kb',
#  'kg',
#  'kr',
#  'CET_CBTL2',
#  'CET_CBTL1',
#  'CET_L19',
#  'CET_L17',
#  'CET_L18',
#  'CET_R2',
#  'rainbow',


# new_attractor_btn = dcc.Button('New Attractor', id='new-attractor-val', n_clicks=0)

# cmap_dropdown = dcc.Dropdown(
#         id='color-dropdown',
#         options=[{'label':x, 'value':x} for x in big_cmaps],
#         value='rainbow')

# gif_length_slider = dcc.Slider("Gif Length", id='gif-length', min=50, max=400, step=1, value=100)
# gif_speed_slider = dcc.Slider("Gif Speed", id='gif-speed', min=1, max=100, step=1, value=50)
# gif_last_frame_linger = dcc.Input(id='gif-last-frame-linger', type='number', value=10)


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


#     html.Button('New Attractor', id='submit-val', n_clicks=0),
#     cmap_dropdown,


#     html.Div(id='inital-params',children='',style={'display': 'none'}),
#     html.Div(id='agg-params',children='',style={'display': 'none'}),


#     dbc.Row([
#             dbc.Col(html.H6(
#              children=[
#               #http://www.pickover.com/
# html.A("This program uses Cliff Pickover's formula",href="http://www.pickover.com/"),
# html.Br(),
#     'x = sin(a * y) + c * np.cos(a * x)',html.Br(),
#     'y = np.sin(b * x) + d * np.cos(b * y)',html.Br(),

#    ' Fractals work by you starting with some initial conditions I start with x[0] and y[0] = 0 and 4 other set parameters a,b,c, and d.'
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
#    ' Too big and slow for Heroku who im using to host this site and turn it into a google cloud serverless api function call.',html.Br(),
#
#    ' I want people to be able to generate and color there own fractals and admire',
#    ' their beauty as I do with every one.'

#              ])
#                     , className="mb-5 mt-5")
#         ]),

# ])

# @app.callback(
#     [Output('inital-params', 'children'),Output('agg-params', 'children')],
#     [Input('submit-val', 'n_clicks')])
# def new_frac(value):
#     #x = requests.get('https://us-central1-atrractors.cloudfunctions.net/function-1?message=0')
#     #agg = eval(x.text)
#     print('clicks', value)
#     if value == 0:
#         #make a random number
#         vals = init_list[random.randint(0, len(init_list))]
#     else:
#         vals = gen_random()

#     #agg = make_detailed(vals)
#     str_vals = str(vals[:])[1:-1].replace(', ','#')
#     agg = ''
#     while len(agg) <= 1:
#         x = requests.get('https://us-central1-atrractors.cloudfunctions.net/function-1?message=' + str_vals)
#         agg = eval(x.text)


#     return vals, json.dumps(agg)

# @app.callback(
#     Output('frac', 'src'),
#     [Input('color-dropdown', 'value'),
#     Input('inital-params', 'children'),
#     Input('agg-params', 'children')])
# def color_figure(color, vals, agg):
#     print('len agg:', len(agg))
#     agg = eval(agg)
#     out = make_pretty(color, vals, agg).to_pil()
#     return out


# @app.callback(
#     Output('gif', 'src'),
#     [Input('gif-length', 'value'),
#     Input('gif-speed', 'value'),
#     Input('gif-last-frame-linger', 'value'),
#     Input('color-dropdown', 'value'),
#     Input('inital-params', 'children'),
#     Input('agg-params', 'children')])
# def make_gif(gif_length, gif_speed, gif_last_frame_linger, color, vals, agg):
#     print('len agg:', len(agg))

#     return out
