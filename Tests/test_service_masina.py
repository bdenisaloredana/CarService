from Domain.masina import Masina
from Domain.validare_masina import ValidareMasina
from Repository.repository_json import RepositoryJson
from Service.service_masina import ServiceMasina
from Service.service_undo_redo import ServiceUndoRedo
from utils import clear_file


def test_service_masina():
    service_undo_redo = ServiceUndoRedo()
    repository_masina = RepositoryJson('test_service_masina.json')
    clear_file('test_service_masina.json')
    validare_masina = ValidareMasina()
    service = ServiceMasina(repository_masina, validare_masina,
                            service_undo_redo)
    service.adaugare_masina('1', 'model1', '2020', 70000, 'da')
    m1 = Masina('1', 'model1', '2020', 70000, 'da')
    assert repository_masina.read('1') == m1
    service.actualizeaza_masina('1', 'model1', '2019', 180, 'nu')
    m2 = Masina('1', 'model1', '2019', 180, 'nu')
    assert repository_masina.read('1') == m2
    service.sterge_masina('1')
    assert repository_masina.read('1') is None
    service.adaugare_masina('1', 'model1', '2020', 70000, 'da')
    service.adaugare_masina('2', 'model2', '2020', 5000, 'nu')
    lista = service.cautare_full_text('1')
    assert len(lista) == 1
    assert lista[0] == m1
    service.actualizare_garantie()
    lista = service.get_all()
    assert lista[0].in_garantie == 'nu'
    assert lista[1].in_garantie == 'da'
