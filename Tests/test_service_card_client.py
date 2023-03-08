from Domain.card_client import CardClient
from Domain.validare_card_client import ValidareCardClient
from Domain.validare_tranzactie import ValidareTranzactie
from Repository.repository_json import RepositoryJson
from Service.service_card_client import ServiceCardClient
from Service.service_tranzactie import ServiceTranzactie
from Service.service_undo_redo import ServiceUndoRedo
from utils import clear_file


def test_service_card_client():
    service_undo_redo = ServiceUndoRedo()
    repository_carduri = RepositoryJson('test_service_card_client.json')
    clear_file('test_service_card_client.json')
    validare_carduri = ValidareCardClient()
    validare_tranzactie = ValidareTranzactie()
    repository_tranzactie = RepositoryJson('test_tr.json')
    clear_file('test_tr.json')
    repository_masina = RepositoryJson('test_ma.json')
    clear_file('test_mas.json')
    service_tranzactie = ServiceTranzactie(repository_tranzactie,
                                           validare_tranzactie,
                                           repository_masina,
                                           service_undo_redo)
    service = ServiceCardClient(repository_carduri, validare_carduri,
                                service_tranzactie, service_undo_redo)

    service.adaugare_card_client('1', 'nume1', 'prenume1',
                                 '6767564563', '23.05.2019', '30.09.2000')
    c1 = CardClient('1', 'nume1', 'prenume1', '6767564563',
                    '23.05.2019', '30.09.2000')
    assert repository_carduri.read('1') == c1
    service.actualizeaza_card_client('1', 'nume2', 'prenume2',
                                     '6767564563', '23.05.2019', '30.09.2000')
    c2 = CardClient('1', 'nume2', 'prenume2', '6767564563',
                    '23.05.2019', '30.09.2000')
    assert repository_carduri.read('1') == c2
    service.adaugare_card_client('2', 'nume2', 'prenume1',
                                 '45443522342', '30.04.2018', '15.02.1986')
    lista = service.cautare_full_text('nume2')
    assert len(lista) == 2
    service.sterge_card_client('1')
    service.sterge_card_client('2')
    assert repository_carduri.read('1') is None
    assert repository_carduri.read('2') is None
    service.adaugare_card_client('1', 'nume1', 'prenume1',
                                 '6767564563', '23.05.2019', '30.09.2000')
    service.adaugare_card_client('2', 'nume2', 'prenume1',
                                 '45443522342', '30.04.2018', '15.02.1986')
    service_tranzactie.adaugare_tranzactie('1', '1', '1', 150.90, 500,
                                           '12.01.2020', '15.00')
    service_tranzactie.adaugare_tranzactie('2', '2', '2', 200, 700,
                                           '09.10.2021', '12.00')
    lst = service.ord_carduri_desc_dupa_reduceri()
    assert lst[0][1] == 70
    assert lst[1][1] == 50
