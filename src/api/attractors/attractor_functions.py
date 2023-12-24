# As said in the README.md, these equations are not mine, most of this project is copy pasted from
# https://examples.holoviz.org/attractors/attractors.html
# and they took it from - https://paulbourke.net/fractals/
import enum
from math import cos, fabs, sin, sqrt

import numpy as np
from numba import jit

# some update to look into  @jit(float32(float32, float32)) takes two floats and returns a float


@jit(nopython=True)
def Clifford(x, y, a, b, c, d, *o):
    return np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)


@jit(nopython=True)
def De_Jong(x, y, a, b, c, d, *o):
    """De Jong attractors From Peter de Jong - http://paulbourke.net/fractals/peterdejong."""
    return sin(a * y) - cos(b * x), sin(c * x) - cos(d * y)


@jit(nopython=True)
def Svensson(x, y, a, b, c, d, *o):
    """Svensson attractors From Johnny Svensson."""
    return d * sin(a * x) - sin(b * y), c * cos(a * x) + cos(b * y)


@jit(nopython=True)
def Bedhead(x, y, a, b, *o):
    """From Ivan Emrich https://www.deviantart.com/jaguarfacedman and
    Jason Rampe https://softologyblog.wordpress.com/2017/03/04/2d-strange-attractors"""
    return sin(x * y / b) * y + cos(a * x - y), x + sin(y) / b


@jit(nopython=True)
def Fractal_Dream(x, y, a, b, c, d, *o):
    """From Clifford A. Pickover's book “Chaos In Wonderland”,
    with parameters from Jason Rampe https://softologyblog.wordpress.com/2017/03/04/2d-strange-attractors
    """
    return sin(y * b) + c * sin(x * b), sin(x * a) + d * sin(y * a)


@jit(nopython=True)
def Hopalong1(x, y, a, b, c, *o):
    """From Barry Martin, here with code for two variants from
    François Pacull https://aetperf.github.io/2018/08/29/Plotting-Hopalong-attractor-with-Datashader-and-Numba.html
    """
    return y - sqrt(fabs(b * x - c)) * np.sign(x), a - x


@jit(nopython=True)
def Hopalong2(x, y, a, b, c, *o):
    return y - 1.0 - sqrt(fabs(b * x - 1.0 - c)) * np.sign(x - 1.0), a - x - 1.0


class AttractorFunctions(str, enum.Enum):
    """Possible attractor functions"""

    CLIFFORD = Clifford
    HOPALONG1 = Hopalong1
    DE_JONG = De_Jong
