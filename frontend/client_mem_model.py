from dataclasses import dataclass
from typing import List

@dataclass
class ClientMemModel:
    """Client side memory model"""
    initial_conditions: List[float]