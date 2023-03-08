from datetime import datetime
import random

from Domain.operatie_adaugare import OperatieAdaugare
from Domain.masina import Masina
from Repository.repository import Repository
from Service.service_undo_redo import ServiceUndoRedo


class Random:
    def __init__(self, repository_masina: Repository,
                 service_undo_redo: ServiceUndoRedo):
        '''
        Constructor.
        :param repository_masina: repository-ul de masinii
        '''

        self.repository_masina = repository_masina
        self.service_undo_redo = service_undo_redo

    def random_masini(self, inceput, n: int) -> None:
        '''
        Genereaza n masini random.
        :param n: cate masini genereaza
        :return: masinile generate
        '''

        an_curent = datetime.now().year
        garantie = ['da', 'nu']
        model_masina = ['ford focus', 'volswagen golf', 'audi q8']

        for i in range(inceput, n+1):
            id_m = str(i)
            x = random.randint(0, 1)
            in_garantie = garantie[x]
            nr_model = random.randint(0, 2)
            model = model_masina[nr_model]
            an = str(random.randint(2000, an_curent))
            nr_km = random.randint(0, 10000)

            masina = Masina(id_m, model, an, nr_km, in_garantie)
            self.repository_masina.create(masina)
            self.service_undo_redo.clear_redo()
            adaugare_operatie = OperatieAdaugare(self.repository_masina,
                                                 masina)
            self.service_undo_redo.add_to_undo(adaugare_operatie)
