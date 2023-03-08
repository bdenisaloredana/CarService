from Domain.tranzactie import Tranzactie
from Domain.validare_masina import ValidareMasina
from Domain.validare_tranzactie import ValidareTranzactie
from Repository.repository_json import RepositoryJson
from Service.service_masina import ServiceMasina
from Service.service_tranzactie import ServiceTranzactie
from Service.service_undo_redo import ServiceUndoRedo
from utils import clear_file


def test_service_tranzactie():
    service_undo_redo = ServiceUndoRedo()
    repository_tr = RepositoryJson('test_service_tranzactie.json')
    repository_masina = RepositoryJson('test.json')
    clear_file('test_service_tranzactie.json')
    clear_file('test.json')
    validare_tranzactie = ValidareTranzactie()
    validare_mas = ValidareMasina()
    service_tr = ServiceTranzactie(repository_tr,
                                   validare_tranzactie, repository_masina,
                                   service_undo_redo)
    service_ma = ServiceMasina(repository_masina, validare_mas,
                               service_undo_redo)
    service_ma.adaugare_masina('1', 'm1', '2020', 1500, 'nu')
    service_ma.adaugare_masina('2', 'm2', '2021', 2000, 'nu')

    service_tr.adaugare_tranzactie('1', '1', '0', 150.90,
                                   500, '12.01.2020', '15.00')
    t1 = Tranzactie('1', '1', '0', 150.9, 450.00, '12.01.2020', '15.00')
    assert repository_tr.read('1') == t1
    service_tr.actualizeaza_tranzactie('1', '1', '0', 200,
                                       700, '09.10.2021', '12.00')
    t2 = Tranzactie('1', '1', '0', 200, 700, '09.10.2021', '12.00')
    assert repository_tr.read('1') == t2
    service_tr.sterge_tranzactie('1')
    assert repository_tr.read('1') is None
    service_tr.adaugare_tranzactie('1', '1', '0', 150.90, 500,
                                   '12.01.2020', '15.00')
    service_tr.adaugare_tranzactie('2', '2', '0', 200, 700,
                                   '09.10.2021', '12.00')
    lista = service_tr.tranzactii_cu_suma_in_interval(0, 700)
    assert len(lista) == 1
    assert lista[0] == Tranzactie(id_entitate='1', id_masina='1',
                                  id_card_client='0', suma_piese=150.9,
                                  suma_manopera=450.00,
                                  data_tranzactie='12.01.2020',
                                  ora_tranzactie='15.00')
    lst = service_tr.ordoneaza_desc_dupa_suma_manopera()
    assert lst[0][1] == 630
    assert lst[1][1] == 450
    service_tr.stergere_tranzactii_din_interval('01.10.2021', '09.10.2021')
    assert len(service_tr.get_all()) == 1
    assert repository_tr.read('1') == t1
    service_tr.adaugare_tranzactie('2', '1', 'null', 500,
                                   800, '12.10.2020', '11:00')
    service_tr.delete_in_cascada('1')
    assert len(service_tr.get_all()) == 0
    service_ma.adaugare_masina('1', 'fs', '2000', 23223, 'nu')
    service_tr.adaugare_tranzactie('1', '12', '1', 900, 1000,
                                   '10.11.2021', '17:45')
    service_tr.delete_in_cascada('1')
    assert len(service_tr.get_all()) == 1
