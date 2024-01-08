import enum
from typing import List

from pydantic import BaseModel


class ColorMap(str, enum.Enum):
    """Possible color map values"""

    FIRE = "fire"
    VIRIDIS = "viridis"
    CET_C1s = "CET_C1s"
    CET_C2 = "CET_C2"
    COLORWHEEL = "colorwheel"
    CET_C4s = "CET_C4s"
    BKR = "bkr"
    INFERNO = "inferno"


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


class InitialConditionsRequest(BaseModel):
    function: str = "Clifford"  # default value
    percent_empty: float = 0.0


class AttractorRequestModel(BaseModel):
    initial_conditions: List[float]
    color_map: str = "fire"  # ColorMap
    # iterations: int = 10000000
    function: str = "Clifford"


class AttractorResponseModel(BaseModel):
    # fileResponse: Response  # -- this crashes the whole thing i guess you cant put fileResponse in a pydantic Model
    initial_conditions: List[float]
