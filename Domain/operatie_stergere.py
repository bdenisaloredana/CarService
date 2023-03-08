from Domain.entitate import Entitate
from Domain.operatie_undo_redo import UndoRedo
from Repository.repository import Repository


class OperatieStergere(UndoRedo):
    def __init__(self, repository: Repository,
                 entitate_stearsa: Entitate):
        '''
        Constructor pentru operatia de stergere.
        :param repository: repository pentru entitati
        :param entitate_stearsa: entitatea stearsa
        '''
        self.repository = repository
        self.entitate_stearsa = entitate_stearsa

    def undo(self) -> None:
        '''
        Adauga inapoi entitatea stearsa.
        '''
        self.repository.create(self.entitate_stearsa)

    def redo(self) -> None:
        '''
        Sterge din nou entitatea, dupa operatia de adaugare din undo.
        '''
        self.repository.delete(self.entitate_stearsa.id_entitate)
