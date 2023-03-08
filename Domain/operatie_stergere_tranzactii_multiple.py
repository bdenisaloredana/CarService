from typing import List

from Domain.operatie_undo_redo import UndoRedo
from Domain.tranzactie import Tranzactie
from Repository.repository import Repository


class OperatieStergereTranzactiiMultiple(UndoRedo):

    def __init__(self, repository: Repository,
                 lista_tranzactii_sterse: List[Tranzactie]):
        '''
        Constructor pentru operatia de stergere tranzactii multiple.
        :param repository: repository de tranzactii
        :param lista_tranzactii_sterse: lista cu tranzactiile sterse
        '''
        self.repository = repository
        self.lista_tranzactii_sterse = lista_tranzactii_sterse

    def undo(self) -> None:
        '''
        Adauga inapoi tranzactiile sterse.
        '''
        for tranzactie in self.lista_tranzactii_sterse:
            self.repository.create(tranzactie)

    def redo(self) -> None:
        '''
        Sterge din nou tranzactiile adaugate in urma operatiei de undo.
        '''
        for tranzactie in self.lista_tranzactii_sterse:
            self.repository.delete(tranzactie.id_entitate)
