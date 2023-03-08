from typing import List

from Domain.masina import Masina
from Domain.operatie_undo_redo import UndoRedo
from Domain.tranzactie import Tranzactie
from Repository.repository import Repository


class OperatieStergereInCascada(UndoRedo):

    def __init__(self, repository_tranzactii: Repository,
                 lista_tranzactii_sterse: List[Tranzactie], masina: Masina,
                 repository_masini: Repository):
        '''
        Constructor pentru operatia de stergere in cascada.
        :param repository_tranzactii: repository-ul tranzactiilor
        :param lista_tranzactii_sterse: lista cu tranzactiile care au fost
        sterse
        :param masina: masina care a fost stearsa
        :param repository_masini: repository-ul masinilor
        '''
        self.repository_tranzactii = repository_tranzactii
        self.lista_tranzactii_sterse = lista_tranzactii_sterse
        self.masina = masina
        self.repository_masini = repository_masini

    def undo(self) -> None:
        '''
        Adauga inapoi masina si tranzactiile sterse.
        '''
        for tranzactie in self.lista_tranzactii_sterse:
            self.repository_tranzactii.create(tranzactie)
        self.repository_masini.create(self.masina)

    def redo(self) -> None:
        '''
        Revine din nou la varianta repository-ului fara tranzactiile din
        lista_Tranzactii_sterse si fara masina.
        '''
        for tranzactie in self.lista_tranzactii_sterse:
            self.repository_tranzactii.delete(tranzactie.id_entitate)
        self.repository_masini.delete(self.masina.id_entitate)
