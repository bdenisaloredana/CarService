from Domain.entitate import Entitate
from Domain.operatie_undo_redo import UndoRedo
from Repository.repository import Repository


class OperatieActualizare(UndoRedo):

    def __init__(self, repository: Repository,
                 entitate_actualizata: Entitate,
                 entitate_anterioara: Entitate):
        '''
        Constructor pentru operatia de actualizare.
        :param repository: un repository pentru entitati
        :param entitate_actualizata: entitatea actualizata
        :param entitate_anterioara: entitatea de dinaintea actualizarii
        '''
        self.repository = repository
        self.entitate_actualizata = entitate_actualizata
        self.entitate_anterioara = entitate_anterioara

    def undo(self) -> None:
        '''
        Revine la entitatea de dinaintea actualizarii.
        '''
        self.repository.update(self.entitate_anterioara)

    def redo(self) -> None:
        '''
        Revine la entitatea de dupa actualizare.
        '''
        self.repository.update(self.entitate_actualizata)
