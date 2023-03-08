from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Masina(Entitate):
    '''
    Creeaza o masina.
    id_masina: id-ul masinii, trebuie sa fie unic
    model: modelul masinii
    an_achizitie: anul achizitiei masinii
    nr_km: numarul de km al masinii
    in_garantie: daca se afla sau nu in garantie
    '''

    model: str
    an_achizitie: str
    nr_km: float
    in_garantie: str
