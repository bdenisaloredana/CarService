from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Tranzactie(Entitate):
    '''
    Creeaza o tranzactie.
    id_tranzactie: id-ul tranzactiei, trebuie sa fie unic
    id_masina: id-ul masinii, trebuie sa fie unic
    id_card_client: id-ul cardului de client, trebuie sa fie unic
    suma_piese: suma pieselor masinii
    suma_manopera: suma manoperei
    data_tranzactie: data tranzactiei
    ora_tranzactie: ora tranzactiei
    '''

    id_masina: str
    id_card_client: str
    suma_piese: float
    suma_manopera: float
    data_tranzactie: str
    ora_tranzactie: str
