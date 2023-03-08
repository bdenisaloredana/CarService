from Domain.tranzactie import Tranzactie
from Repository.repository_json import RepositoryJson
from utils import clear_file


def test_repository_tranzactie():
    filename = 'test_repository_tranzactie.json'
    clear_file(filename)
    tranzactii = RepositoryJson(filename)
    t1 = Tranzactie('1', '3', '2', 150.4, 200, '12.12.2020', '15.40')
    tranzactii.create(t1)
    assert tranzactii.read(t1.id_entitate) == t1
    t2 = Tranzactie('2', '4', '1', 1000, 500, '04.06.2021', '20.20')
    tranzactii.create(t2)
    assert tranzactii.read(t2.id_entitate) == t2
    t3 = Tranzactie('2', '4', '1', 10, 550, '04.06.2021', '20.30')
    tranzactii.update(t3)
    tranzactie = tranzactii.read(t3.id_entitate)
    assert tranzactie == t3
    tranzactii.delete(t2.id_entitate)
    assert tranzactii.read('2') is None
    tranzactii.delete(t1.id_entitate)
    assert tranzactii.read('1') is None
