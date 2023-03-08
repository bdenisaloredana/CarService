from abc import ABC
from dataclasses import dataclass


@dataclass
class Entitate(ABC):
    '''
    Creeaza o entitate.
    '''
    id_entitate: str
