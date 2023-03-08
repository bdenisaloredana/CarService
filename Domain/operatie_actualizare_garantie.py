from typing import List

from Domain.masina import Masina
from Domain.operatie_undo_redo import UndoRedo
from Repository.repository import Repository


class OperatieActualizareGarantie(UndoRedo):

    def __init__(self, repository: Repository,
                 lista_masini_anterioare: List[Masina],
                 lista_masini_actualizate: List[Masina]):
        '''
        Constructor pentru operatia de actualizare garantie.
        :param repository: repository-ul pentru masini
        :param lista_masini_anterioare: lista cu masinile inaintea
        actualizarii garantiei
        :param lista_masini_actualizate: lista cu masinile dupa
        actualizarea garantiei
        '''
        self.repository = repository
        self.lista_masini_anterioare = lista_masini_anterioare
        self.lista_masini_actualizate = lista_masini_actualizate

    def undo(self) -> None:
        '''
        Revine la masinile de dinaintea actualizarii garantiei.
        '''
        for masina in self.lista_masini_anterioare:
            self.repository.update(masina)

    def redo(self) -> None:
        '''
        Revine la masinile de dupa actualizarea garantiei.
        '''
        for masina in self.lista_masini_actualizate:
            self.repository.update(masina)
