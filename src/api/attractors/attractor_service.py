import sys
from io import BytesIO
from typing import Callable, List

import datashader as ds
import numpy as np
import pandas as pd
from colorcet import palette
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis
from loguru import logger
from numba import jit
from pandas import DataFrame

palette["viridis"] = viridis
palette["inferno"] = inferno


@jit(nopython=True)
def trajectory_coords(fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n: int = 10000000):
    x, y = np.zeros(n), np.zeros(n)
    x[0], y[0] = x0, y0
    for i in np.arange(n - 1):
        x[i + 1], y[i + 1] = fn(x[i], y[i], a, b, c, d, e, f)
    return x, y


class AttractorService:
    def __init__(self):
        self.n = 10000000

    def trajectory(self, fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=10000000):
        x, y = trajectory_coords(fn, x0, y0, a, b, c, d, e, f, n)
        return pd.DataFrame(dict(x=x, y=y))

    def gen_random(self, func, desired_empty=10000):
        # finds some nice inital conditions
        non_empty = 0
        # how many non empty pixels
        while non_empty < desired_empty:
            inital_conditions = np.c_[
                np.zeros((1, 2)), np.random.random((1, 6)) * 4 - 2
            ][0]
            logger.info(f"inital_conditions: {inital_conditions}")
            # small n for quick generations of inital conditions
            df = self.trajectory(func, *inital_conditions, n=20000)
            cvs = ds.Canvas(plot_width=500, plot_height=500)
            agg = cvs.points(df, "x", "y")
            non_empty = np.count_nonzero(np.array(agg))
            logger.info(f"non_empty: {non_empty}")
        return inital_conditions

    def make_dataframe(
        self, inital_conditions: List[float], function: Callable, label=True
    ):
        """Return a Datashader image by collecting `n` trajectory points for the given attractor `fn`"""
        lab = (
            ("{}, " * (len(inital_conditions) - 1) + " {}").format(*inital_conditions)
            if label
            else None
        )
        logger.info(f"label: {lab}")
        df = self.trajectory(function, *inital_conditions, n=self.n)  # type: ignore
        return df

    def df_to_imgs(self, df: DataFrame, cmap: str):
        imgs = []
        cvs = ds.Canvas(plot_width=500, plot_height=500)
        # we dont want every point plotted to be a frame so this makes 45 frames between 200 and n
        for i in np.geomspace(200, self.n, 45).astype(int):
            agg = cvs.points(df[:i], "x", "y")
            color_map = palette[cmap]
            imgs.append(tf.shade(agg, cmap=color_map).to_pil())
            # palette[color_map]

        # pad out final image to make it last longer
        imgs.append(imgs[-1])
        imgs.append(imgs[-1])
        imgs.append(imgs[-1])
        imgs.append(imgs[-1])
        imgs.append(imgs[-1])
        print(len(df))
        print("df size", sys.getsizeof(df))
        return imgs

    def make_gif_from_df(self, df: DataFrame, cmap: str) -> BytesIO:
        imgs = self.df_to_imgs(df, cmap=cmap)
        fp_out = BytesIO()
        imgs[0].save(
            fp=fp_out,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=300,
            loop=1,
        )
        return fp_out
