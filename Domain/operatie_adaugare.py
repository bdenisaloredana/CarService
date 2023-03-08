from Domain.entitate import Entitate
from Domain.operatie_undo_redo import UndoRedo
from Repository.repository import Repository


class OperatieAdaugare(UndoRedo):

    def __init__(self, repository: Repository,
                 entitate_adaugata: Entitate):
        '''
        Constructor pentru operatia de adaugare.
        :param repository: repository pentru entitati
        :param entitate_adaugata: entitatea adaugata
        '''
        self.repository = repository
        self.entitate_adaugata = entitate_adaugata

    def undo(self) -> None:
        '''
        Sterge entitatea adaugata.
        '''
        self.repository.delete(self.entitate_adaugata.id_entitate)

    def redo(self) -> None:
        '''
        Readauga entitatea stearsa, dupa operatia de undo.
        '''
        self.repository.create(self.entitate_adaugata)
