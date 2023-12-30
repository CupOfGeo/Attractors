from dataclasses import asdict, dataclass
from typing import List


@dataclass
class ClientMemModel:
    """Client side memory model"""

    initial_conditions: List[float]

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return ClientMemModel(**d)
