from datetime import datetime
from typing import List
from Domain.operatie_adaugare import OperatieAdaugare
from Domain.masina import Masina
from Domain.operatie_actualizare import OperatieActualizare
from Domain.operatie_actualizare_garantie import OperatieActualizareGarantie
from Domain.operatie_stergere import OperatieStergere
from Domain.validare_masina import ValidareMasina
from Repository.exceptii import TextGol, FisierGol
from Repository.repository import Repository
from Service.service_undo_redo import ServiceUndoRedo


class ServiceMasina:
    def __init__(self, repository_masina: Repository,
                 validare_masina: ValidareMasina,
                 service_undo_redo: ServiceUndoRedo):
        '''
        Constructor.
        :param repository_masina: repository-ul masinii
        :param validare_masina: validator masina
        :param service_undo_redo: service-ul pentru operatiile de undo si
        redo
        '''

        self.repository_masina = repository_masina
        self.validare_masina = validare_masina
        self.service_undo_redo = service_undo_redo

    def adaugare_masina(self, id_masina: str, model: str,
                        an_achizitie: str, nr_km: float,
                        in_garantie: str) -> None:
        '''
        Adauga o masina la o lista de masini.
        :param id_masina: id-ul masinii
        :param model: modelul masinii
        :param an_achizitie: anul achizitiei masinii
        :param nr_km: numarul de km al masinii
        :param in_garantie: daca se afla sau nu in garantie- da sau nu
        :return: lista de masini in urma adaugarii
                 masinii ce contine parametrii de mai sus
        '''

        masina = Masina(id_masina, model, an_achizitie, nr_km, in_garantie)
        self.validare_masina.valideaza(masina)
        self.repository_masina.create(masina)
        self.service_undo_redo.clear_redo()
        adauga_operatie = OperatieAdaugare(self.repository_masina,
                                           masina)
        self.service_undo_redo.add_to_undo(adauga_operatie)

    def actualizeaza_masina(self, id_masina: str, model: str,
                            an_achizitie: str, nr_km: float,
                            in_garantie: str) -> None:
        '''
        Actualizeaza o masina din lista de masini.
        :param id_masina: id-ul masinii
        :param model: modelul masinii
        :param an_achizitie: anul achizitiei masinii
        :param nr_km: numarul de km al masinii
        :param in_garantie: daca se afla sau nu in garantie- da sau nu
        :return: lista de masini cu masina care are id-ul id_masina actualizata
        '''

        masina_anterioara = self.repository_masina.read(id_masina)
        masina = Masina(id_masina, model, an_achizitie, nr_km, in_garantie)
        self.validare_masina.valideaza(masina)
        self.repository_masina.update(masina)
        operatie = OperatieActualizare(self.repository_masina, masina,
                                       masina_anterioara)
        self.service_undo_redo.add_to_undo(operatie)

    def sterge_masina(self, id_masina) -> None:
        '''
        Sterge o masina din lista de masini.
        :param id_masina: id-ul masinii pe care dorim sa o stergem
        :return: lista in urma stergerii masinii cu id-ul id_masina
        '''
        masina = self.repository_masina.read(id_masina)
        self.repository_masina.delete(id_masina)
        adauga_operatie = OperatieStergere(self.repository_masina, masina)
        self.service_undo_redo.add_to_undo(adauga_operatie)

    def get_all(self) -> List[Masina]:
        '''
        Citeste masinile.
        :return: masinile
        '''

        return self.repository_masina.read()

    def cautare_full_text(self, string) -> List[Masina]:
        '''
        Cauta un string in masinile din lista.
        :param string: string-ul pe care il cauta
        :return: o lista care contine masinile in care apare string-ul
        '''

        if string == '':
            raise TextGol('Textul cautat nu poate fi gol')

        masini = self.get_all()
        if len(masini) == 0:
            raise FisierGol('Nu exista masini')

        lista = [masina for masina in masini if string in
                 masina.id_entitate or string in masina.model or string in
                 masina.in_garantie or string in str(masina.nr_km) or
                 string in masina.an_achizitie]

        return lista

    def actualizare_garantie(self) -> None:
        '''
        Actualizeaza garantia la fiecare masina:o mașină este în garanție
        dacă are maxim 3 ani de la achiziție și maxim 60 000 de km.
        :return: masinile cu garantia actualizata
        '''

        masini = self.get_all()
        if len(masini) == 0:
            raise FisierGol('Nu exista masini')
        an = datetime.now().year
        an_minim_garantie = an - 3

        lista_masini_anterioare = [masina for masina in masini]
        lista_masini_actualizate = []

        for m in masini:
            an_achizitie = int(m.an_achizitie)
            if an_achizitie >= an_minim_garantie and an_achizitie <= an:
                if m.nr_km <= 60000:
                    m.in_garantie = 'da'
                else:
                    m.in_garantie = 'nu'
            else:
                m.in_garantie = 'nu'

            masina = Masina(m.id_entitate, m.model,
                            m.an_achizitie, m.nr_km, m.in_garantie)
            self.repository_masina.update(masina)
            lista_masini_actualizate.append(self.repository_masina.read(
                masina.id_entitate))

        operatie = OperatieActualizareGarantie(self.repository_masina,
                                               lista_masini_anterioare,
                                               lista_masini_actualizate)
        self.service_undo_redo.add_to_undo(operatie)
