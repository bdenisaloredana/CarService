from dataclasses import dataclass
from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    '''
    Creeaza un card client.
    id_card_client: id-ul cardului de client, trebuie sa fie unic
    nume: numele clientului
    prenume: prenumele clientului
    cnp: cnp-ul clientului
    data_inregistrare: data inregistrarii cardului
    data_nastere: data nasterii clientului
    '''

    nume: str
    prenume: str
    cnp: str
    data_inregistrare: str
    data_nastere: str
