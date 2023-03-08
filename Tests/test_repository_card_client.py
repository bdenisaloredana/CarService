from Domain.card_client import CardClient
from Repository.repository_json import RepositoryJson
from utils import clear_file


def test_repository_card_client():
    filename = 'test_repository_card.json'
    clear_file(filename)
    carduri_client = RepositoryJson(filename)
    c1 = CardClient('1', 'nume1', 'prenume1',
                    '6546546566575', '12.08.2015', '01.15.1990')
    carduri_client.create(c1)
    assert carduri_client.read(c1.id_entitate) == c1
    c2 = CardClient('2', 'nume2', 'prenume2',
                    '4534556546008', '12.11.2020', '08.15.2000')
    carduri_client.create(c2)
    assert carduri_client.read(c2.id_entitate) == c2
    c3 = CardClient('2', 'nume3', 'prenume3',
                    '4534556546008', '12.11.2020', '08.15.2000')
    carduri_client.update(c3)
    card = carduri_client.read(c2.id_entitate)
    assert card == c3
    carduri_client.delete(c2.id_entitate)
    assert carduri_client.read('2') is None
    carduri_client.delete(c1.id_entitate)
    assert carduri_client.read('1') is None
