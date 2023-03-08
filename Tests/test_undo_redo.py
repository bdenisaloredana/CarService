from Domain.masina import Masina
from Domain.operatie_actualizare import OperatieActualizare
from Domain.operatie_actualizare_garantie import OperatieActualizareGarantie
from Domain.operatie_adaugare import OperatieAdaugare
from Domain.operatie_stergere import OperatieStergere
from Domain.operatie_stergere_tranzactii_multiple import \
    OperatieStergereTranzactiiMultiple
from Domain.tranzactie import Tranzactie
from Domain.validare_masina import ValidareMasina
from Domain.validare_tranzactie import ValidareTranzactie
from Repository.repository_json import RepositoryJson
from Service.service_masina import ServiceMasina
from Service.service_tranzactie import ServiceTranzactie
from Service.service_undo_redo import ServiceUndoRedo
from utils import clear_file


def test_undo_redo():

    service_undo_redo = ServiceUndoRedo()
    repository = RepositoryJson('test_undo_redo.json')
    clear_file('test_undo_redo.json')
    repository_masina = RepositoryJson('test_undo_redo_masina.json')
    clear_file('test_undo_redo_masina.json')
    validare_masina = ValidareMasina()
    service_masina = ServiceMasina(repository_masina, validare_masina,
                                   service_undo_redo)

    # testare adaugare
    service_masina.adaugare_masina('1', 'model1', '2020', 70000, 'da')
    m1 = Masina('1', 'model1', '2020', 70000, 'da')
    operatie1 = OperatieAdaugare(repository_masina, m1)
    service_undo_redo.add_to_undo(operatie1)
    service_masina.adaugare_masina('2', 'model2', '2020', 5000, 'nu')
    assert len(service_masina.get_all()) == 2
    m2 = Masina('2', 'model2', '2020', 5000, 'nu')
    operatie2 = OperatieAdaugare(repository_masina, m2)
    service_undo_redo.add_to_undo(operatie2)
    service_undo_redo.do_undo()
    assert len(service_masina.get_all()) == 1
    service_undo_redo.do_redo()
    assert len(service_masina.get_all()) == 2

    # testare actualizare
    m2_actualizata = Masina('2', 'model100', '2021', 0, 'da')
    operatie_actualizare = OperatieActualizare(repository_masina,
                                               m2_actualizata,
                                               m2)
    service_masina.actualizeaza_masina('2', 'model100', '2021', 0, 'da')
    service_undo_redo.add_to_undo(operatie_actualizare)
    assert repository_masina.read('2') == Masina(id_entitate='2',
                                                 model='model100',
                                                 an_achizitie='2021',
                                                 nr_km=0, in_garantie='da')
    service_undo_redo.do_undo()
    assert repository_masina.read('2') == Masina(id_entitate='2',
                                                 model='model2',
                                                 an_achizitie='2020',
                                                 nr_km=5000, in_garantie='nu')
    service_undo_redo.do_redo()
    assert repository_masina.read('2') == Masina(id_entitate='2',
                                                 model='model100',
                                                 an_achizitie='2021',
                                                 nr_km=0, in_garantie='da')
    # testare stergere
    masina = repository_masina.read('2')
    service_masina.sterge_masina('2')
    operatie_stergere = OperatieStergere(repository_masina, masina)
    service_undo_redo.add_to_undo(operatie_stergere)
    assert len(service_masina.get_all()) == 1
    service_undo_redo.do_undo()
    assert len(service_masina.get_all()) == 2
    service_undo_redo.do_redo()
    assert len(service_masina.get_all()) == 1
    service_undo_redo.do_undo()

    # testare actualizare garantie
    lista_masini_anterioare = []
    m1 = repository_masina.read('1')
    m2 = repository_masina.read('2')
    lista_masini_anterioare.append(m1)
    lista_masini_anterioare.append(m2)
    service_masina.actualizare_garantie()
    lista_masini_actualizate = service_masina.get_all()
    assert lista_masini_actualizate[0].in_garantie == 'nu'
    assert lista_masini_actualizate[1].in_garantie == 'da'
    operatie_actualizare_garantie = OperatieActualizareGarantie(
        repository_masina, lista_masini_anterioare, lista_masini_actualizate)
    service_undo_redo.add_to_undo(operatie_actualizare_garantie)
    service_undo_redo.do_undo()
    lista = service_masina.get_all()
    assert lista[0] == lista_masini_anterioare[0]
    assert lista[1] == lista_masini_anterioare[1]
    service_undo_redo.do_redo()
    masina1 = repository_masina.read('1')
    assert masina1.in_garantie == 'nu'

    # testare stergere tranzactii multiple
    repository_tr = RepositoryJson('test_undo_redo_tranzactie.json')
    repository_masina = RepositoryJson('test_undo_redo_rep_masina.json')
    clear_file('test_undo_redo_tranzactie.json')
    clear_file('test_undo_redo_rep_masina.json')
    validare_tranzactie = ValidareTranzactie()
    validare_mas = ValidareMasina()
    service_tr = ServiceTranzactie(repository_tr,
                                   validare_tranzactie, repository_masina,
                                   service_undo_redo)
    service_ma = ServiceMasina(repository_masina, validare_mas,
                               service_undo_redo)
    service_ma.adaugare_masina('1', 'm1', '2020', 1500, 'nu')
    service_ma.adaugare_masina('2', 'm2', '2021', 2000, 'nu')

    service_tr.adaugare_tranzactie('1', '1', '0', 150.90, 500,
                                   '12.01.2020', '15.00')
    service_tr.adaugare_tranzactie('2', '2', '0', 200, 700,
                                   '09.10.2021', '12.00')
    service_tr.adaugare_tranzactie('3', '2', '0', 10000, 4023,
                                   '10.10.2021', '14:00')
    t1 = Tranzactie('1', '1', '0', 150.90, 500, '12.01.2020', '15.00')
    t2 = Tranzactie('2', '2', '1', 200, 700, '09.10.2021', '12.00')
    t3 = Tranzactie('3', '2', '1', 10000, 4023, '10.10.2021', '14:00')
    lista_tranzactii_sterse = []
    service_tr.stergere_tranzactii_din_interval('01.10.2021', '10.10.2021')
    assert len(service_tr.get_all()) == 1
    lista_tranzactii_sterse.append(t2)
    lista_tranzactii_sterse.append(t3)
    operatie_stergere_multipla = OperatieStergereTranzactiiMultiple(
        repository_tr, lista_tranzactii_sterse)
    service_undo_redo.add_to_undo(operatie_stergere_multipla)
    service_undo_redo.do_undo()
    assert len(service_tr.get_all()) == 3
    service_undo_redo.do_redo()
    assert len(service_tr.get_all()) == 1
    service_undo_redo.do_undo()

    # testare stergere in cascada
    lista_tranzactii_sterse = []
    service_tr.delete_in_cascada('1')
    lista_tranzactii_sterse.append(t2)
    lista_tranzactii_sterse.append(t3)
    service_tr.delete_in_cascada('2')
    assert len(service_tr.get_all()) == 0
    operatie_stergere_m = OperatieStergereTranzactiiMultiple(
        repository_tr, lista_tranzactii_sterse)
    service_undo_redo.add_to_undo(operatie_stergere_m)
    service_undo_redo.do_undo()
    assert len(service_tr.get_all()) == 2
    service_undo_redo.do_redo()
    assert len(service_tr.get_all()) == 0
