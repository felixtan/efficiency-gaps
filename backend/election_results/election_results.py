import abc

class ElectionResults(abc.ABC):
    def __init__(self, type, year, state, legislative_body_code, district=None):
        pass
