from Repository.exceptii import ValoarePozitiva, OraInvalida, TextGol, \
    DataInvalida, IdDuplicat, NuExistaId, FisierGol, GarantieInvalida
from Service.generare_random_masini import Random
from Service.service_card_client import ServiceCardClient
from Service.service_masina import ServiceMasina
from Service.service_tranzactie import ServiceTranzactie
from Service.service_undo_redo import ServiceUndoRedo


class Console:
    def __init__(self, service_masina: ServiceMasina,
                 service_tranzactie: ServiceTranzactie,
                 service_card_client: ServiceCardClient,
                 service_undo_redo: ServiceUndoRedo,
                 random: Random,
                 ):
        '''
        Constructor.
        :param service_masina: service-ul masinii
        :param service_tranzactie: service-ul tranzactiei
        :param service_card_client: service-ul cardului de client
        :param service_undo_redo: service-ul pentru operatiile de undo si
        redo
        '''
        self.service_masina = service_masina
        self.service_tranzactie = service_tranzactie
        self.service_card_client = service_card_client
        self.service_undo_redo = service_undo_redo
        self.random = random

    def show_menu(self):
        print('a(m/t/c) - adaugare masina/tranzactie/card client (ex. am)')
        print('u(m/t/c) - update masina/tranzactie/card client (ex. ut)')
        print('d(m/t/c) - stergere masina/tranzactie/card client (ex. dt)')
        print('s(m/t/c) - show all masina/tranzactie/card client (ex. sm)')
        print('1. Cautare full text')
        print('2. Afișare tranzacții cu suma cuprinsă într-un interval dat')
        print('3. Afișarea mașinilor ordonate descrescător după suma manoperă')
        print('4. Afișarea cardurilor client ordonate descrescător'
              ' după valoarea reducerilor obținute')
        print('5. Ștergerea tuturor tranzacțiilor '
              'dintr-un anumit interval de zile')
        print('6. Actualizarea garanție masini ')
        print('g. Generare n masini random')
        print('u. Undo')
        print('r. Redo')
        print('x. Iesire')

    def run_console(self):
        while True:
            self.show_menu()
            optiune = input('Dati optiune ')

            if optiune == 'am':
                self.handle_add_masina()
            elif optiune == 'at':
                self.handle_add_tranzactie()
            elif optiune == 'ac':
                self.handle_add_card_client()
            elif optiune == 'um':
                self.handle_update_masina()
            elif optiune == 'ut':
                self.handle_update_tranzactie()
            elif optiune == 'uc':
                self.handle_update_card_client()
            elif optiune == 'dm':
                self.handle_delete_masina()
            elif optiune == 'dt':
                self.handle_delete_tranzactie()
            elif optiune == 'dc':
                self.handle_delete_card_client()
            elif optiune == 'sm':
                self.handle_show_all(self.service_masina.get_all())
            elif optiune == 'st':
                self.handle_show_all(self.service_tranzactie.get_all())
            elif optiune == 'sc':
                self.handle_show_all(self.service_card_client.get_all())
            elif optiune == '1':
                self.handle_cautare_full_text()
            elif optiune == '2':
                self.handle_afisare_tranzactii()
            elif optiune == '3':
                self.handle_masini_ordonate_desc()
            elif optiune == '4':
                self.handle_carduri_ordonate_desc()
            elif optiune == '5':
                self.handle_stergere_tranzactii_din_interval()
            elif optiune == '6':
                self.handle_actualizare_garantie()
            elif optiune == 'g':
                self.handle_random()
            elif optiune == 'u':
                self.service_undo_redo.do_undo()
            elif optiune == 'r':
                self.service_undo_redo.do_redo()
            elif optiune == 'x':
                break
            else:
                print('Optiune invalida')

    def handle_add_masina(self):
        try:
            id_m = input('Dati id-ul masinii ')
            model = input('Dati modelul masinii ')
            an_achizitie = input('Dati anul achizitiei masinii ')
            km = float(input('Dati numarul de km al masinii '))
            garantie = input('Masina este in garantie da/nu ')

            self.service_masina.adaugare_masina(id_m, model,
                                                an_achizitie, km, garantie)
            print(f'Masina cu id-ul {id_m} a fost adaugata.')

        except ValoarePozitiva as vp:
            print('Valoare pozitiva: ', vp)
        except GarantieInvalida as gi:
            print('Garantie invalida: ', gi)
        except DataInvalida as d:
            print('Data invalida: ', d)
        except TextGol as tg:
            print('Text gol: ', tg)
        except IdDuplicat as di:
            print('Id duplicat: ', di)
        except Exception as e:
            print('Eroare: ', e)

    def handle_show_all(self, obiecte):
        if len(obiecte) == 0:
            print('Lista este goala.')
        else:
            for obiect in obiecte:
                print(obiect)

    def handle_add_tranzactie(self):
        try:
            id_t = input('Dati id-ul tranzactiei ')
            id_masina = input('Dati id-ul masinii ')
            id_card = input('Dati id-ul cardului clientului  ')
            suma_p = float(input('Dati suma pieselor '))
            suma_m = float(input('Dati suma manoperei '))
            data = input('Dati data tranzactiei ')
            ora = input('Dati ora tranzactiei ')
            if id_card != 'null':
                print('Exista un card client si '
                      'se aplica 10% reducere pentru manopera.')

            self.service_tranzactie.adaugare_tranzactie(id_t, id_masina,
                                                        id_card, suma_p,
                                                        suma_m, data, ora)
            tranzactii = self.service_tranzactie.get_all()
            for tranzactie in tranzactii:
                if tranzactie.id_entitate == id_t:
                    tr = tranzactie

            if tr.suma_piese == 0:
                print('Masina este in garantie, iar piesele sunt gratis.')

            print(f'Tranzactia cu id-ul {id_t} a fost adaugata.')

        except ValoarePozitiva as vp:
            print('Valoare pozitiva: ', vp)
        except OraInvalida as oi:
            print('Ora invalida: ', oi)
        except TextGol as tg:
            print('Text gol: ', tg)
        except DataInvalida as d:
            print('Data invalida: ', d)
        except IdDuplicat as di:
            print('Id duplicat: ', di)
        except Exception as e:
            print('Eroare: ', e)

    def handle_add_card_client(self):
        try:
            id_c = input('Dati id-ul cardului clientului ')
            nume = input('Dati numele clientului ')
            prenume = input('Dati prenumele clientului ')
            cnp = input('Dati CNP-ul clientului ')
            data_n = input('Dati data nasterii clientului ')
            data_i = input('Dati data inregistrarii clientului ')
            self.service_card_client.adaugare_card_client(id_c, nume,
                                                          prenume, cnp,
                                                          data_i, data_n)
            print(f'Cardul client cu id-ul {id_c} a fost adaugat.')

        except TextGol as tg:
            print('Text gol: ', tg)
        except DataInvalida as d:
            print('Data invalida: ', d)
        except IdDuplicat as di:
            print('Id duplicat: ', di)
        except Exception as e:
            print('Eroare: ', e)

    def handle_update_masina(self):
        try:
            id_m = input('Dati id-ul masinii ')
            model = input('Dati modelul masinii ')
            an_a = input('Dati anul achizitiei masinii ')
            km = float(input('Dati numarul de km al masinii '))
            garantie = input('Masina este in garantie da/nu ')

            self.service_masina.actualizeaza_masina(id_m, model,
                                                    an_a, km, garantie)
            print(f'Masina cu id-ul {id_m} a fost actualizata.')

        except ValoarePozitiva as vp:
            print('Valoare pozitiva: ', vp)
        except GarantieInvalida as gi:
            print('Garantie invalida: ', gi)
        except DataInvalida as d:
            print('Data invalida: ', d)
        except TextGol as tg:
            print('Text gol: ', tg)
        except NuExistaId as nei:
            print('Nu exista id-ul: ', nei)
        except Exception as e:
            print('Eroare: ', e)

    def handle_update_tranzactie(self):
        try:
            id_t = input('Dati id-ul tranzactiei ')
            id_m = input('Dati id-ul masinii ')
            id_card = input('Dati id-ul cardului clientului  ')
            suma_p = float(input('Dati suma pieselor '))
            suma_m = float(input('Dati suma manoperei'))
            data = input('Dati data tranzactiei ')
            ora = input('Dati ora tranzactiei ')
            self.service_tranzactie.actualizeaza_tranzactie(id_t, id_m,
                                                            id_card, suma_p,
                                                            suma_m, data, ora)
            print(f'Tranzactia cu id-ul {id_t} a fost actualizata.')

        except ValoarePozitiva as vp:
            print('Valoare pozitiva: ', vp)
        except OraInvalida as oi:
            print('Ora invalida: ', oi)
        except TextGol as tg:
            print('Text gol: ', tg)
        except DataInvalida as d:
            print('Data invalida: ', d)
        except NuExistaId as nei:
            print('Nu exista id-ul: ', nei)
        except Exception as e:
            print('Eroare: ', e)

    def handle_update_card_client(self):
        try:
            id_c = input('Dati id-ul cardului clientului ')
            nume = input('Dati numele clientului ')
            prenume = input('Dati prenumele clientului ')
            cnp = input('Dati CNP-ul clientului ')
            data_n = input('Dati data nasterii clientului ')
            data_i = input('Dati data inregistrarii clientului ')

            self.service_card_client.actualizeaza_card_client(id_c,
                                                              nume, prenume,
                                                              cnp, data_i,
                                                              data_n)
            print(f'Cardul client cu id-ul {id_c} a fost actualizat.')

        except TextGol as tg:
            print('Text gol: ', tg)
        except DataInvalida as d:
            print('Data invalida: ', d)
        except NuExistaId as nei:
            print('Nu exista id-ul: ', nei)
        except Exception as e:
            print('Eroare: ', e)

    def handle_delete_masina(self):
        try:
            id_m = input('Dati id-ul masinii'
                         ' pe care doriti sa o stergeti ')

            self.service_tranzactie.delete_in_cascada(id_m)
            print(f'Masina cu id-ul {id_m} si toate tranzactiile '
                  f'aferente acesteia au fost sterse.')

        except NuExistaId as nei:
            print('Nu exista id-ul: ', nei)
        except Exception as e:
            print('Eroare: ', e)

    def handle_delete_tranzactie(self):
        try:
            id_t = input('Dati id-ul tranzactiei'
                         ' pe care doriti sa o stergeti ')
            self.service_tranzactie.sterge_tranzactie(id_t)
            print(f'Tranzactia cu id-ul {id_t} a fost stearsa.')

        except NuExistaId as nei:
            print('Nu exista id-ul: ', nei)
        except Exception as e:
            print('Eroare: ', e)

    def handle_delete_card_client(self):
        try:
            id_c = input('Dati id-ul cardului de client'
                         ' pe care doriti sa il stergeti ')
            self.service_card_client.sterge_card_client(id_c)
            print(f'Cardul client cu id-ul {id_c} a fost sters.')

        except NuExistaId as nei:
            print('Nu exista id-ul: ', nei)
        except Exception as e:
            print('Eroare: ', e)

    def handle_cautare_full_text(self):
        try:
            string = input('Dati text ')
            masini = self.service_masina.cautare_full_text(string)
            carduri = self.service_card_client.cautare_full_text(string)

            if len(carduri) == 0 and len(masini) == 0:
                print('Nu exista masini si clienti gasiti in urma cautarii.')
            else:
                print('Masinile si clientii gasiti in urma cautarii sunt:')
                if len(masini) != 0:
                    self.handle_show_all(masini)
                if len(carduri) != 0:
                    self.handle_show_all(carduri)

        except TextGol as tg:
            print('Text gol: ', tg)
        except FisierGol as fg:
            print('Fisier gol: ', fg)
        except Exception as e:
            print('Eroare: ', e)

    def handle_afisare_tranzactii(self):
        try:
            st = float(input('Dati capatul din stanga al intervalului '))
            dr = float(input('Dati capatul din dreapta al intervalului '))
            lst = self.service_tranzactie.tranzactii_cu_suma_in_interval(st,
                                                                         dr)
            print(f'Tranzactiile cu suma cuprinsa '
                  f'in intervalul [{int(st)}, {int(dr)}] sunt:')
            self.handle_show_all(lst)

        except ValoarePozitiva as vp:
            print('Valoare pozitiva: ', vp)
        except FisierGol as fg:
            print('Fisier gol: ', fg)
        except Exception as e:
            print('Eroare: ', e)

    def handle_random(self):
        try:
            n = int(input('Dati numar n '))
            lista = self.service_masina.get_all()
            print(len(lista))
            self.random.random_masini(len(lista) + 1, n + len(lista))
            print('Masinile generate sunt:')
            self.handle_show_all(self.service_masina.get_all())
        except KeyError as ke:
            print('Eroare de id: ', ke)
        except Exception as e:
            print('Eroare: ', e)

    def handle_masini_ordonate_desc(self):
        try:
            lista = self.service_tranzactie.ordoneaza_desc_dupa_suma_manopera()
            print('Lista cu masinile ordonate '
                  'descrescator dupa suma manopera este:')
            for element in lista:
                print(f'{element[0]},suma manopera:{element[1]}.')
        except FisierGol as fg:
            print('Fisier gol: ', fg)
        except Exception as e:
            print('Eroare: ', e)

    def handle_actualizare_garantie(self):
        try:
            self.service_masina.actualizare_garantie()
            self.handle_show_all(self.service_masina.get_all())
        except FisierGol as fg:
            print('Fisier gol: ', fg)
        except Exception as e:
            print('Eroare: ', e)

    def handle_stergere_tranzactii_din_interval(self):
        try:
            stg = input('Dati data de inceput ')
            dr = input('Dati data de sfarsit ')
            self.service_tranzactie.stergere_tranzactii_din_interval(stg, dr)
            self.handle_show_all(self.service_tranzactie.get_all())
        except FisierGol as fg:
            print('Fisier gol: ', fg)
        except DataInvalida as dv:
            print('Data invalida: ', dv)
        except Exception as e:
            print('Eroare: ', e)

    def handle_carduri_ordonate_desc(self):
        try:
            lst = self.service_card_client.ord_carduri_desc_dupa_reduceri()
            print('Lista cu cardurile ordonate descrescator'
                  ' dupa valoarea reducerilor obtinute este:')
            for element in lst:
                print(f'{element[0]}, valoarea reducerilor: {element[1]}')

        except FisierGol as fg:
            print('Fisier gol : ', fg)
        except Exception as e:
            print('Eroare: ', e)
