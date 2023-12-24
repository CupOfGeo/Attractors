import enum
from typing import List

from pydantic import BaseModel


class AttractorFunction(str, enum.Enum):
    """Possible attractor function values"""
    CLIFFORD = 'Clifford'
    AIZAWA = 'Aizawa'
    DE_JONG = 'De_Jong'
    LORENZ = 'Lorenz'
    ROSSLER = 'Rossler'
    THOMAS = 'Thomas'
    HALVORSEN = 'Halvorsen'
    LUE = 'Lue'
    CHUA = 'Chua'
    DADRA = 'Dadra'
    FOUR_WING = 'Four_Wing'
    FOUR_SCROLL = 'Four_Scroll'
    HADLEY = 'Hadley'
    LIU_CHEN = 'Liu_Chen'
    LORENZ_84 = 'Lorenz_84'
    RUCKLIDGE = 'Rucklidge'
    ARNEODO = 'Arneodo'
    BURKE_SHAW = 'Burke_Shaw'
    CHEN_LEE = 'Chen_Lee'
    CHEN = 'Chen'
    CHEN_CELIKOVIC = 'Chen_Celikovic'
    COULLET = 'Coullet'
    DUFFING = 'Duffing'
    DUFFING_84 = 'Duffing_84'
    DUFFING_JULIA = 'Duffing_Julia'
    DUFFING_VANDERPOL = 'Duffing_Vanderpol'
    HALVORSEN_WEYER = 'Halvorsen_Weyer'
    HENON = 'Henon'
    HINDMARSH_ROSE = 'Hindmarsh_Rose'
    HINDMARSH_ROSE_84 = 'Hindmarsh_Rose_84'
    HINDMARSH_ROSE_89 = 'Hindmarsh_Rose_89'
    HINDMARSH_ROSE_89_1 = 'Hindmarsh_Rose_89_1'
    HINDMARSH_ROSE_89_2 = 'Hindmarsh_Rose_89_2'
    HINDMARSH_ROSE_89_3 = 'Hindmarsh_Rose_89_3'
    HINDMARSH_ROSE_89_4 = 'Hindmarsh_Rose_89_4'
    HINDMARSH_ROSE_89_5 = 'Hindmarsh_Rose_89_5'
    HINDMARSH_ROSE_89


class ColorMap(str, enum.Enum):
    """Possible color map values"""
    FIRE = 'fire'
    VIRIDIS = 'viridis'
    CET_C1s = 'CET_C1s'
    CET_C2 = 'CET_C2'
    COLORWHEEL = 'colorwheel'
    CET_C4s = 'CET_C4s'
    BKR = 'bkr'
    INFERNO = 'inferno'
#  'bky'
#  'CET_D13'
#  'CET_D1A'
#  'coolwarm'
#  'CET_D9'
#  'CET_D10'
#  'diverging_gkr_60_10_c40'
#  'CET_D3'
#  'gwv'
#  'diverging_isoluminant_cjm_75_c24'
#  'CET_D11'
#  'CET_D8'
#  'bjy'
#  'CET_R3'
#  'CET_I1'
#  'CET_I3'
#  'bgy'
#  'linear_bgyw_15_100_c67'
#  'bgyw'
#  'CET_L9'
#  'kbc'
#  'blues'
#  'CET_L7'
#  'bmw'
#  'CET_L8'
#  'bmy'
#  'kgy'
#  'gray'
#  'dimgray'
#  'CET_L16'
#  'kgy'
#  'CET_L4'
#  'linear_kry_5_95_c72'
#  'linear_kry_5_98_c75'
#  'fire'
# 'inferno'
#  'linear_kryw_5_100_c64'
#  'linear_kryw_5_100_c67'
#  'CET_CBL1'
#  'CET_CBL2'
#  'kb'
#  'kg'
#  'kr'
#  'CET_CBTL2'
#  'CET_CBTL1'
#  'CET_L19'
#  'CET_L17'
#  'CET_L18'
#  'CET_R2'
#  'rainbow'
#  'CET_R1'
#  'rainbow_bgyrm_35_85_c71'


class AttractorRequestModel(BaseModel):
    initial_conditions: List[float]
    color_map: ColorMap
    # iterations: int = 10000000
    function: str = 'Clifford'


class AttractorResponseModel(BaseModel):
    # fileResponse: Response  # -- this crashs the whole thing i guess you cant put fileResponse in a pydantic Model
    inital_conditions: List[float]
