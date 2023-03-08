from abc import ABC, abstractmethod


class UndoRedo(ABC):

    @abstractmethod
    def undo(self):
        ...

    @abstractmethod
    def redo(self):
        ...
