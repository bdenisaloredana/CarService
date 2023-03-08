from Domain.masina import Masina
from Repository.repository_json import RepositoryJson
from Service.generare_random_masini import Random
from Service.service_undo_redo import ServiceUndoRedo
from utils import clear_file


def test_repository_masina():
    service_undo_redo = ServiceUndoRedo()
    filename = 'test_repository.json'
    clear_file(filename)
    repository = RepositoryJson(filename)
    m1 = Masina('1', 'model1', '2004', 100, 'da')
    repository.create(m1)
    assert repository.read(m1.id_entitate) == m1
    m2 = Masina('2', 'model2', '2020', 0, 'nu')
    repository.create(m2)
    assert repository.read(m2.id_entitate) == m2
    m3 = Masina('2', 'model2', '2020', 50, 'nu')
    repository.update(m3)
    masina = repository.read(m2.id_entitate)
    assert masina == m3
    random = Random(repository, service_undo_redo)
    random.random_masini(3, 4)
    i = 0
    for masina in repository.read():
        i = 1 + i
    assert i == 4
    repository.delete(m2.id_entitate)
    assert repository.read('2') is None
    repository.delete(m1.id_entitate)
    assert repository.read('1') is None
