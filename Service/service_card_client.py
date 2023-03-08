from typing import List, Tuple
from Domain.operatie_adaugare import OperatieAdaugare
from Domain.card_client import CardClient
from Domain.operatie_actualizare import OperatieActualizare
from Domain.operatie_stergere import OperatieStergere
from Domain.validare_card_client import ValidareCardClient
from Repository.exceptii import TextGol, FisierGol
from Repository.repository import Repository
from Service.service_tranzactie import ServiceTranzactie
from Service.service_undo_redo import ServiceUndoRedo
from sortare import sortare


class ServiceCardClient:
    def __init__(self, repository_carduri: Repository,
                 validare_card_client: ValidareCardClient,
                 service_tranzactie: ServiceTranzactie,
                 service_undo_redo: ServiceUndoRedo):
        '''
        Constructor.
        :param repository_carduri: repository-ul cardului de client
        :param validare_card_client: validator card client
        :param service_undo_redo: service-ul pentru operatiile de undo si
        redo
        '''

        self.repository_carduri = repository_carduri
        self.validare_card_client = validare_card_client
        self.service_tranzactie = service_tranzactie
        self.service_undo_redo = service_undo_redo

    def adaugare_card_client(self, id_card_client: str, nume: str,
                             prenume: str, cnp: str,
                             data_inregistrare: str,
                             data_nastere: str) -> None:
        '''
        Adauga un card client la lista de carduri.
        :param id_card_client: id-ul cardului de client
        :param nume: numele clientului
        :param prenume: prenumele clientului
        :param cnp: cnp-ul clientului
        :param data_inregistrare: data de inregistrare a cardului
        :param data_nastere: data de nastere a clientului
        :return: lista de carduri in urma adaugarii
                 cardului client ce contine parametrii de mai sus
        '''

        card_client = CardClient(id_card_client, nume, prenume,
                                 cnp, data_inregistrare, data_nastere)
        self.validare_card_client.valideaza(card_client)
        self.repository_carduri.create(card_client)
        self.service_undo_redo.clear_redo()
        adauga_operatie = OperatieAdaugare(self.repository_carduri,
                                           card_client)
        self.service_undo_redo.add_to_undo(adauga_operatie)

    def actualizeaza_card_client(self, id_card_client: str, nume: str,
                                 prenume: str, cnp: str,
                                 data_inregistrare: str,
                                 data_nastere: str) -> None:
        '''
        Actualizeaza un card client dintr-o lista de carduri.
        :param id_card_client: id-ul cardului de client
        :param nume: numele clientului
        :param prenume: prenumele clientului
        :param cnp: cnp-ul clientului
        :param data_inregistrare: data de inregistrare a cardului
        :param data_nastere: data de nastere a clientului
        :return: lista de carduri cu cardul care are id-ul
                 id_card_client actualizat
        '''

        card_anterior = self.repository_carduri.read(id_card_client)
        card_client = CardClient(id_card_client, nume, prenume,
                                 cnp, data_inregistrare, data_nastere)
        self.validare_card_client.valideaza(card_client)
        self.repository_carduri.update(card_client)
        operatie = OperatieActualizare(self.repository_carduri,
                                       card_client, card_anterior)
        self.service_undo_redo.add_to_undo(operatie)

    def sterge_card_client(self, id_card_client) -> None:
        '''
        Sterge un card client din lista de carduri.
        :param id_card_client: id-ul cardului de client
        :return: lista de carduri fara cardul cu id-ul id_card_client
        '''
        card = self.repository_carduri.read(id_card_client)
        self.repository_carduri.delete(id_card_client)
        adauga_operatie = OperatieStergere(self.repository_carduri, card)
        self.service_undo_redo.add_to_undo(adauga_operatie)

    def get_all(self) -> List[CardClient]:
        '''
        Citeste cardurile de client.
        :return: cardurile de client
        '''

        return self.repository_carduri.read()

    def cautare_full_text(self, string) -> List[CardClient]:
        '''
        Cauta un string in cardurile din lista.
        :param string: string-ul pe care il cauta
        :return: o lista care contine cardurile in care apare string-ul
        '''

        if string == '':
            raise TextGol('Textul cautat nu poate fi gol')

        carduri = self.get_all()
        if len(carduri) == 0:
            raise FisierGol('Nu exista carduri')

        lista = [card for card in carduri if string in card.id_entitate or
                 string in card.nume or string in card.prenume or string in
                 card.cnp or string in card.data_inregistrare or string in
                 card.data_nastere]

        return lista

    def ord_carduri_desc_dupa_reduceri(self) -> List[Tuple]:
        '''
        Ordoneaza descrescator cardurile client
        dupa valoarea reducerilor obtinute.
        :return:returneaza cardurile ordonate descrescator dupa valoarea
                reducerilor obtinute
        '''

        def lista_tranzactii_corespunzatoare(tranzactii) -> List[Tuple]:
            '''
            Determina tranzactiile a caror id_card_client
            exista in repository-ul de cadruri si nu este null.
            :param tranzactii: lista de tranzactii
            :return: -o lista goala atunci cand nu exista tranzactii
                     -o lista de tupluri de forma(card, valoarea reducerii)
                     in caz contrar
            '''
            if not tranzactii:
                return []

            tranzactie = tranzactii[0]
            if tranzactie.id_card_client != 'null' and \
                    self.repository_carduri.read(tranzactie.id_card_client)\
                    is not None:

                suma = (tranzactie.suma_manopera * 100) / 90
                valoare_reducere = suma - tranzactie.suma_manopera
                card = self.repository_carduri.read(
                    tranzactie.id_card_client)

                return [(card, valoare_reducere)] + \
                    lista_tranzactii_corespunzatoare(tranzactii[1:])
            else:
                return lista_tranzactii_corespunzatoare(tranzactii[1:])

        def verificare(lista, lst_ids) -> List[Tuple]:
            '''
            Verifica daca in lista exista mai multe tranzactii carora ii
            corespund acelasi id_card_client, iar daca da, aduna toate
            reduceriile obtinute pentru cardurile cu acelasi id, astfel
            ramanand doar unul.
            :param lista: lista de tranzacii
            :param lst_ids: lista de id-uri pentru carduri
            :return: -o lista goala daca nu exista tranzactii
                     -o lista de tupluri de forma(card, suma valoarilor
                     reducerilor) in caz contrar
            '''
            if len(lista) == 0:
                return []

            el = lista[0]
            if el[0].id_entitate not in str(lst_ids):
                valoare_reduceri = [tuplu[1] for tuplu in lista if tuplu[0]
                                    == el[0]]
                suma = sum(valoare_reduceri)
                return [(el[0], suma)] + verificare(lista[1:], lst_ids +
                                                    list(el[0].id_entitate))
            else:
                return verificare(lista[1:], lst_ids)

        tranzactii = self.service_tranzactie.get_all()
        carduri = self.get_all()

        if len(tranzactii) == 0:
            raise FisierGol('Nu exista tranzactii')
        if len(carduri) == 0:
            raise FisierGol('Nu exista carduri')

        lst_ids = []
        lista = lista_tranzactii_corespunzatoare(tranzactii)
        lista_2 = verificare(lista, lst_ids)

        return sortare(lista_2, key=lambda x: x[1], reverse=True)
