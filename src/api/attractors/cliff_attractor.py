import sys

import datashader as ds
import numpy as np
import numpy.random
import pandas as pd
from colorcet import palette
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis
from numba import jit
from pandas import DataFrame

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


def make_dataframe(vals, n=n, cmap='inferno', label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    n = 4000000
    ("{}, " * (len(vals) - 1) + " {}").format(*vals) if label else None
    # print(lab)
    df = trajectory(Clifford, *vals, n)
    return df


def to_ds(df: DataFrame, cmap='inferno'):
    imgs = []
    cvs = ds.Canvas(plot_width=500, plot_height=500)
    # we dont want every point plotted to be a frame so this makes 45 frames between 200 and n
    for i in np.geomspace(200, n, 45).astype(int):
        agg = cvs.points(df[:i], 'x', 'y')
        color_map = palette[cmap]
        imgs.append(tf.shade(agg, cmap=color_map))
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


def make_gif_from_df(df: DataFrame, cmap='inferno'):
    imgs = to_ds(df, cmap=cmap)
    for i in range(len(imgs)):
        imgs[i] = imgs[i].to_pil()
    fp_out = "content/flip_gif_temp.gif"
    imgs[0].save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=300, loop=1)
    return None


def myplot(fn, vals, n=n, cmap='inferno', label=True):
    """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
    n = 4000000
    imgs = []
    lab = ("{}, " * (len(vals) - 1) + " {}").format(*vals) if label else None
    # print(lab)
    df = trajectory(fn, *vals, n)
    cvs = ds.Canvas(plot_width=500, plot_height=500)
    # we dont want every point plotted to be a frame so this makes 45 frames between 200 and n
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
