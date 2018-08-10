import abc

class CooperativeConstructor(abc.ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
