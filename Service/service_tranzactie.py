from typing import List, Tuple
from Domain.operatie_adaugare import OperatieAdaugare
from Domain.operatie_actualizare import OperatieActualizare
from Domain.operatie_stergere import OperatieStergere
from Domain.operatie_stergere_in_cascada import OperatieStergereInCascada
from Domain.operatie_stergere_tranzactii_multiple import \
    OperatieStergereTranzactiiMultiple
from Domain.tranzactie import Tranzactie
from Domain.validare_tranzactie import ValidareTranzactie
from Repository.exceptii import FisierGol, ValoarePozitiva, DataInvalida
from Repository.repository import Repository
from Service.service_undo_redo import ServiceUndoRedo
from sortare import sortare


class ServiceTranzactie:
    def __init__(self, repository_tranzactie: Repository,
                 validare_tranzactie: ValidareTranzactie,
                 repository_masina: Repository,
                 service_undo_redo: ServiceUndoRedo):
        '''
        Constructor.
        :param repository_tranzactie: repository-ul tranzactiei
        :param validare_tranzactie: validator tranzactie
        :param repository_masina: repository-ul masinii
        :param service_undo_redo: service-ul pentru operatiile de undo si
        redo
        '''

        self.repository_tranzactie = repository_tranzactie
        self.validare_tranzactie = validare_tranzactie
        self.repository_masina = repository_masina
        self.service_undo_redo = service_undo_redo

    def adaugare_tranzactie(self, id_tranzactie: str, id_masina: str,
                            id_card_client: str, suma_piese: float,
                            suma_manopera: float, data_tranzactie: str,
                            ora_tranzactie: str) -> None:
        '''
        Adauga o tranzactie la lista de tranzactii.
        :param id_tranzactie: id-ul tranzactiei
        :param id_masina: id-ul masinii din cadrul tranzactiei
        :param id_card_client: id-ul cardului de client
        :param suma_piese: suma pieselor masinii
        :param suma_manopera: suma manoperei
        :param data_tranzactie: data tranzactiei
        :param ora_tranzactie: ora tranzactiei
        :return: lista cu tranzactia ce contine parametrii de mai sus adaugata
        '''

        if id_masina != 'null':
            if self.repository_masina.read(id_masina) is not None:
                masina = self.repository_masina.read(id_masina)
                if masina.in_garantie == 'da':
                    suma_piese = 0

        if id_card_client != 'null':
            suma_manopera = (suma_manopera * 90) / 100

        tranzactie = Tranzactie(id_tranzactie, id_masina, id_card_client,
                                suma_piese, suma_manopera,
                                data_tranzactie, ora_tranzactie)

        self.validare_tranzactie.valideaza(tranzactie)
        self.repository_tranzactie.create(tranzactie)
        self.service_undo_redo.clear_redo()
        adauga_operatie = OperatieAdaugare(self.repository_tranzactie,
                                           tranzactie)
        self.service_undo_redo.add_to_undo(adauga_operatie)

    def actualizeaza_tranzactie(self, id_tranzactie: str, id_masina: str,
                                id_card_client: str, suma_piese: float,
                                suma_manopera: float, data_tranzactie: str,
                                ora_tranzactie: str) -> None:
        '''
        Actualizeaza o tranzactie din lista de tranzactii.
        :param id_tranzactie: id-ul tranzactiei
        :param id_masina: id-ul masinii din cadrul tranzactiei
        :param id_card_client: id-ul cardului de client
        :param suma_piese: suma pieselor masinii
        :param suma_manopera: suma manoperei
        :param data_tranzactie: data tranzactiei
        :param ora_tranzactie: ora tranzactiei
        :return: lista cu tranzactia care are id-ul id_tranzactie actualizata
        '''
        tranzactie_anterioara = self.repository_tranzactie.read(
            id_tranzactie)
        tranzactie = Tranzactie(id_tranzactie, id_masina, id_card_client,
                                suma_piese, suma_manopera,
                                data_tranzactie, ora_tranzactie)
        self.validare_tranzactie.valideaza(tranzactie)
        self.repository_tranzactie.update(tranzactie)
        operatie = OperatieActualizare(self.repository_tranzactie,
                                       tranzactie, tranzactie_anterioara)
        self.service_undo_redo.add_to_undo(operatie)

    def sterge_tranzactie(self, id_tranzactie) -> None:
        '''
        Sterge o tranzactie din lista de tranzactii.
        :param id_tranzactie: id-ul tranzactiei pe care dorim sa o stergem
        :return: lista de tranzactii in urma stergerii
                 tranzactiei cu id-ul id_tranzactie
        '''
        tranzactie = self.repository_tranzactie.read(id_tranzactie)
        self.repository_tranzactie.delete(id_tranzactie)
        operatie = OperatieStergere(self.repository_masina,
                                    tranzactie)
        self.service_undo_redo.add_to_undo(operatie)

    def get_all(self) -> List[Tranzactie]:
        '''
        Citeste tranzactiile.
        :return: tranzactiile
        '''

        return self.repository_tranzactie.read()

    def tranzactii_cu_suma_in_interval(self, stanga,
                                       dreapta) -> List[Tranzactie]:
        '''
        Determina tranzactiile a caror suma se afla intr-un interval dat.
        :param stanga: capatul din stanga al intervalului
        :param dreapta: capatul din dreapta al intervalului
        :return: o lista cu tranzactiile a caror suma se incadreaza in
        interval
        '''

        if stanga < 0 or dreapta < 0:
            raise ValoarePozitiva('Capetele intervalului '
                                  'nu pot fi numere negative')

        tranzactii = self.get_all()

        if len(tranzactii) == 0:
            raise FisierGol('Nu exista tranzactii')

        lista = [tranzactie for tranzactie in tranzactii if
                 tranzactie.suma_piese + tranzactie.suma_manopera >= stanga
                 and tranzactie.suma_piese + tranzactie.suma_manopera <=
                 dreapta]

        return lista

    def ordoneaza_desc_dupa_suma_manopera(self) -> List[Tuple]:
        '''
        Ordoneaza descrescator masinile dupa suma obtinuta pe manopera.
        :return: returneaza masinile ordonate descrescator dupa suma obtinuta
                 pe manopera
        '''

        def lista_tranzactii_corespunzatoare(tranzactii) -> List[Tuple]:
            '''
            Determina tranzactiile a caror id_maina
            exista in repository-ul de masini.
            :param tranzactii: lista de tranzactii
            :return: -o lista goala atunci cand nu exista tranzactii
                     -o lista de tupluri de forma(masina, suma obtinuta pe
                     manopera) in caz contrar
            '''
            if not tranzactii:
                return []

            tranzactie = tranzactii[0]
            if self.repository_masina.read(tranzactie.id_masina) is not None:
                return [(self.repository_masina.read(tranzactie.id_masina),
                        tranzactie.suma_manopera)] + \
                       lista_tranzactii_corespunzatoare(tranzactii[1:])
            else:
                return lista_tranzactii_corespunzatoare(tranzactii[1:])

        def verificare(lista, lst_ids: List) -> List[Tuple]:
            '''
            Verifica daca in lista exista mai multe tranzactii carora ii
            corespund acelasi id_masina, iar daca da, aduna toate sumele
            obtinute pe manopera pentru masinile cu acelasi id, astfel
            ramanand doar una.
            :param lista: lista de tranzacii
            :param lst_ids: lista de id-uri pentru masini
            :return: -o lista goala daca nu exista tranzactii
                     -o lista de tupluri de forma(masina, suma manopera
                     totala) in caz contrar
            '''
            if len(lista) == 0:
                return []

            el = lista[0]
            if el[0].id_entitate not in str(lst_ids):
                suma_manopera_completa_element = [tuplu[1] for tuplu in
                                                  lista if tuplu[0] == el[0]]

                suma = sum(suma_manopera_completa_element)
                return [(el[0], suma)] + verificare(lista[1:], lst_ids +
                                                    list(el[0].id_entitate))
            else:
                return verificare(lista[1:], lst_ids)

        tranzactii = self.get_all()
        if len(tranzactii) == 0:
            raise FisierGol('Nu exista tranzactii')

        lista_ids = []
        lista = lista_tranzactii_corespunzatoare(tranzactii)
        lista_2 = verificare(lista, lista_ids)
        return sortare(lista_2, key=lambda x: x[1], reverse=True)

    def stergere_tranzactii_din_interval(self, stanga: str,
                                         dreapta: str) -> None:
        '''
        Sterge toate tranzactiile dintr-un interval de zile.
        :param stanga: capatul din stanga al intervalului
        :param dreapta: capatul din dreapta al intervalului
        :return: tranzactiile fara cele care au fost efectuate
                 in intervalul dat

        '''

        def verifica_data(tranzactie):
            '''
            Verifica daca data tranzactiei este cuprinsa intre datele date
            de la tastatura.
            :param tranzactie: tranzactia care se verifica
            :return: True- daca se afla intre cele doua date, False in caz
            contrar
            '''

            zi_tr = int(tranzactie.data_tranzactie[0:2])
            luna_tr = int(tranzactie.data_tranzactie[3:5])
            an_tr = int(tranzactie.data_tranzactie[6:10])
            if zi_tr >= zi_stg and zi_tr <= zi_dr:
                if luna_tr >= luna_stg and luna_tr <= luna_dr:
                    if an_tr >= an_stg and an_tr <= an_dr:
                        return True
            return False

        tranzactii = self.get_all()
        if len(tranzactii) == 0:
            raise FisierGol('Nu exista tranzactii')
        if len(stanga) < 10 or len(dreapta) < 10:
            raise DataInvalida('Data tranzactie invalida ')

        zi_stg = int(stanga[0:2])
        zi_dr = int(dreapta[0:2])
        luna_stg = int(stanga[3:5])
        luna_dr = int(dreapta[3:5])
        an_stg = int(stanga[6:10])
        an_dr = int(dreapta[6:10])

        lista_tranzactii_de_sters = list(filter(verifica_data, tranzactii))

        for tranzactie in lista_tranzactii_de_sters:
            self.sterge_tranzactie(tranzactie.id_entitate)

        operatie = OperatieStergereTranzactiiMultiple(
            self.repository_tranzactie, lista_tranzactii_de_sters)
        self.service_undo_redo.add_to_undo(operatie)

    def delete_in_cascada(self, id_m: str) -> None:
        '''
        Sterge toate tranzactiile care au id-ul masinii egal cu id_ul dat.
        :param id_m: id_ul masinii
        :return: tranzactiile fara cele ce au id-ul masinii egal cu id_m
        '''

        tranzactii = self.get_all()
        if len(tranzactii) == 0:
            raise FisierGol('Nu exista tranzactii')

        masina = self.repository_masina.read(id_m)
        self.repository_masina.delete(id_m)

        lista_tranzactii_de_sters = [tranzactie for tranzactie in tranzactii
                                     if tranzactie.id_masina == id_m]

        for tranzactie in lista_tranzactii_de_sters:
            self.repository_tranzactie.delete(tranzactie.id_entitate)

        op = OperatieStergereInCascada(self.repository_tranzactie,
                                       lista_tranzactii_de_sters,
                                       masina, self.repository_masina
                                       )
        self.service_undo_redo.add_to_undo(op)
