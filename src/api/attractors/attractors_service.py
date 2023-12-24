
import datashader as ds
import numpy as np
import numpy.random
import pandas as pd
from numba import jit

from src.api.attractors.attractor_functions import Clifford

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


class AttractorService:

    def __init__(self):
        pass

    def gen_random(self, func=Clifford, desired_empty=10000):
        # finds some nice inital conditions
        non_empty = 0

        # how many non empty pixels
        while non_empty < desired_empty:
            rvals = np.c_[np.zeros((1, 2)), numpy.random.random((1, 6)) * 4 - 2]
            agg = init_plot(func, rvals[0], n=20000)
            non_empty = np.count_nonzero(np.array(agg))
        return rvals[0]


AttractorService().gen_random()
