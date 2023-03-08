from typing import Dict
import jsonpickle as jsonpickle
from Domain.entitate import Entitate
from Repository.exceptii import NuExistaId, IdDuplicat
from Repository.repository import Repository


class RepositoryJson(Repository):

    def __init__(self, filename):
        '''
        Constructor.
        :param filename: numele fisierului
        '''

        super().__init__()
        self.filename = filename

    def __read__file(self):
        '''
        Citeste date dintr-un fisier.
        :return: datele
        '''

        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, obiecte: Dict[str, Entitate]):
        '''
        Scrie un obiect intr-un fisier.
        :param objects: obiectele
        '''

        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(obiecte))

    def create(self, entitate: Entitate) -> None:
        '''
        Adauga o entitate la lista de entitati.
        :param entitate: entitate
        :return: o lista de entitati cu entitatea adaugata
        '''

        entitati = self.__read__file()
        if self.read(entitate.id_entitate) is not None:
            raise IdDuplicat(f'Exista deja o entitate cu id_ul'
                             f' {entitate.id_entitate}')

        entitati[entitate.id_entitate] = entitate
        self.__write_file(entitati)

    def read(self, id_entitate=None) -> None:
        '''
        Citeste o entitate.
        :param id_entitate: id-ul entitatii
        :return: -entitatea cu id id_entitate
                  sau None daca id_entitate nu e None;
                 -lista cu toate entitatile daca id_entitate e None
        '''

        entitati = self.__read__file()
        if id_entitate:
            if id_entitate in entitati:
                return entitati[id_entitate]
            else:
                return None

        return list(entitati.values())

    def update(self, entitate: Entitate) -> None:
        '''
        Actualizeaza o entitate.
        :param entitate: entitate
        :return: lista de entitati cu entitatea actualizata
        '''

        entitati = self.__read__file()
        if self.read(entitate.id_entitate) is None:
            raise NuExistaId(f'Nu exista o entitate cu id-ul '
                             f'{entitate.id_entitate} de actualizat')

        entitati[entitate.id_entitate] = entitate
        self.__write_file(entitati)

    def delete(self, id_entitate: int) -> None:
        '''
        Sterge o entitate.
        :param id_entitate: id-ul entitatii
        :return: lista de entitati fara entitatea cu id-ul id_entitate
        '''

        entitati = self.__read__file()
        if self.read(id_entitate) is None:
            raise NuExistaId(f'Nu exista o entitate cu id-ul'
                             f' {id_entitate} pe care sa o stergem')

        del entitati[id_entitate]
        self.__write_file(entitati)
