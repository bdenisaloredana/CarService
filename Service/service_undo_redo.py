from typing import List
from Domain.operatie_undo_redo import UndoRedo


class ServiceUndoRedo:
    def __init__(self):
        '''
        Constructor pentru service-ul de undo si redo.
        '''
        self.lista_undo: List[UndoRedo] = []
        self.lista_redo: List[UndoRedo] = []

    def do_undo(self) -> None:
        '''
        Sterge ultima operatiune facuta.
        '''
        if self.lista_undo:
            operatie = self.lista_undo.pop()
            operatie.undo()
            self.lista_redo.append(operatie)

    def do_redo(self) -> None:
        '''
        Revine la operatiunea de dinaintea stergerii.
        '''
        if self.lista_redo:
            operatie = self.lista_redo.pop()
            operatie.redo()
            self.lista_undo.append(operatie)

    def clear_redo(self) -> None:
        '''

        :return:
        '''
        self.lista_redo.clear()

    def add_to_undo(self, operatie: UndoRedo) -> None:
        '''
        Adauga o operatie la lista de undo.
        :param operatie: operatia care se adauga
        '''
        self.lista_undo.append(operatie)
