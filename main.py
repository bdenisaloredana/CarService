from Domain.validare_card_client import ValidareCardClient
from Domain.validare_masina import ValidareMasina
from Domain.validare_tranzactie import ValidareTranzactie
from Repository.repository_json import RepositoryJson
from Service.generare_random_masini import Random
from Service.service_card_client import ServiceCardClient
from Service.service_masina import ServiceMasina
from Service.service_tranzactie import ServiceTranzactie
from Service.service_undo_redo import ServiceUndoRedo
from Tests.test_repository_card_client import test_repository_card_client
from Tests.test_repository_masina import test_repository_masina
from Tests.test_repository_tranzactie import test_repository_tranzactie
from Tests.test_service_card_client import test_service_card_client
from Tests.test_service_masina import test_service_masina
from Tests.test_service_tranzactie import test_service_tranzactie
from Tests.test_undo_redo import test_undo_redo
from UI.console import Console


def main():

    service_undo_redo = ServiceUndoRedo()

    repository_masina = RepositoryJson('masina.json')
    validare_masina = ValidareMasina()
    service_masina = ServiceMasina(repository_masina, validare_masina,
                                   service_undo_redo)

    repository_tranzactie = RepositoryJson('tranzactie.json')
    validare_tranzactie = ValidareTranzactie()
    service_tranzactie = ServiceTranzactie(repository_tranzactie,
                                           validare_tranzactie,
                                           repository_masina,
                                           service_undo_redo)

    reposiory_card_client = RepositoryJson('card_client.json')
    validare_card_client = ValidareCardClient()
    service_card_client = ServiceCardClient(reposiory_card_client,
                                            validare_card_client,
                                            service_tranzactie,
                                            service_undo_redo)

    random = Random(repository_masina, service_undo_redo)

    console = Console(service_masina, service_tranzactie,
                      service_card_client, service_undo_redo, random)
    console.run_console()


test_undo_redo()
test_service_card_client()
test_service_tranzactie()
test_service_masina()
test_repository_card_client()
test_repository_tranzactie()
test_repository_masina()
main()
