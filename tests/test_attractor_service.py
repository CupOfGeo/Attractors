from src.api.attractors.attractor_functions import Clifford
from src.api.attractors.attractor_service import AttractorService

N = 100
attractor_service = AttractorService(n=N)


def test_gen_random_len():
    result = attractor_service.gen_random(Clifford, desired_empty=1)
    assert len(result) == 8


def test_make_dataframe():
    test_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    result = attractor_service.make_dataframe(test_list, Clifford)
    assert len(result) == N
