import sys

import datashader as ds
import numpy as np
import numpy.random
import pandas as pd
import xarray as xr
from colorcet import palette
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis
from numba import jit

palette["viridis"] = viridis
palette["inferno"] = inferno


@jit(nopython=True)
def Clifford(x, y, a, b, c, d, *o):
    return np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)


n = 10000000


@jit(nopython=True)
def trajectory_coords(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=n):
    x, y = np.zeros(n), np.zeros(n)
    x[0], y[0] = x0, y0
    for i in np.arange(n - 1):
        x[i + 1], y[i + 1] = fn(x[i], y[i], a, b, c, d, e, f)
    return x, y


def trajectory(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=n):
    x, y = trajectory_coords(fn, x0, y0, a, b, c, d, e, f, n)
    return pd.DataFrame(dict(x=x, y=y))


def init_plot(fn, vals, n=n):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    # values_label = ("{}, "*(len(vals)-1)+" {}").format(*vals) if label else None
    df = trajectory(fn, *vals, n=n)
    cvs = ds.Canvas(plot_width=500, plot_height=500)
    agg = cvs.points(df, 'x', 'y')
    return agg


def gen_random(func=Clifford, desired_empty=10000):
    # finds some nice inital conditions thats it
    non_empty = 0

    # how many non empty pixels
    while non_empty < desired_empty:
        rvals = np.c_[np.zeros((1, 2)), numpy.random.random((1, 6)) * 4 - 2]
        agg = init_plot(func, rvals[0], n=20000)
        non_empty = np.count_nonzero(np.array(agg))
    return rvals[0]


# take inital conditions and makes a nice agg
def make_detailed(vals, n=n, cmap=viridis, label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    m = 1000000
    vals[0] = 0
    vals[1] = 0
    cvs = ds.Canvas(plot_width=500, plot_height=500)
    agg_sum = 0
    # for i in np.geomspace(200, m, 100).astype(int):
    for i in range(100):
        # lab = ("{}, "*(len(vals)-1)+" {}"+' n:'+str((1+i)*m)).format(*vals) if label else None
        df = trajectory(Clifford, *vals, n=m)
        vals[0] = df.iloc[m - 1].x
        vals[1] = df.iloc[m - 1].y

        agg = cvs.points(df, 'x', 'y')
        agg_sum = agg.values + agg_sum
    # imgs
    return xr.DataArray(agg_sum)


def make_pretty(color, vals, agg):
    if vals == '':  # or agg == None
        vals = gen_random()
        agg = make_detailed(Clifford, vals)
    if color == '':
        color = 'fire'
    print('vals:', vals)
    lab = ("{}, " * (len(vals) - 1) + " {}").format(*vals) if vals else None
    img = tf.shade(xr.DataArray(agg), cmap=palette[color], name=lab)
    img = tf.set_background(img, 'black')
    return img


def myplot(fn, vals, n=n, cmap='inferno', label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    n = 4000000
    imgs = []
    lab = ("{}, " * (len(vals) - 1) + " {}").format(*vals) if label else None
    # print(lab)
    df = trajectory(fn, *vals, n)
    cvs = ds.Canvas(plot_width=500, plot_height=500)
    for i in np.geomspace(200, n, 45).astype(int):
        agg = cvs.points(df[:i], 'x', 'y')
        color_map = palette[cmap]
        imgs.append(tf.shade(agg, cmap=color_map, name=lab))
        # palette[color_map]

    # pad out final image to make it last longer
    imgs.append(imgs[-1])
    imgs.append(imgs[-1])
    imgs.append(imgs[-1])
    imgs.append(imgs[-1])
    imgs.append(imgs[-1])
    print(len(df))
    print('df size', sys.getsizeof(df))
    return imgs


def make_gif(initial_conditions, cmap='inferno'):
    # initial_conditions = gen_random()
    imgs = myplot(Clifford, initial_conditions, cmap=cmap)
    for i in range(len(imgs)):
        imgs[i] = imgs[i].to_pil()
    fp_out = "content/flip_gif_temp.gif"
    imgs[0].save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=300, loop=1)
    return initial_conditions


# make_gif()
# vals = gen_random()
# im, a, df = init_plot(Clifford, vals, n=10000000)
#
# im = im.to_pil()
# im.save('im.png')
# plot(func, vals=[["kbc"]+list(rvals[i]) for i in range(len(rvals))], label=True) #NOTEBOOK TO FILE
#
# color_map = palette['inferno']
# img = tf.shade(a,cmap=color_map).to_pil()
# img.save('img.png')
#
# img = tf.shade(agg, cmap = viridis).to_pil()
#
# #img = Image.new(mode = "RGB", size = (300,300))
# img.save('img.png')
