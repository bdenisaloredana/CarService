from Domain.tranzactie import Tranzactie
from Repository.exceptii import TextGol, ValoarePozitiva, \
    DataInvalida, OraInvalida


class ValidareTranzactie:

    def valideaza(self, tranzactie: Tranzactie) -> None:
        '''
        Valideaza o tranzactie.
        :param tranzactie: tranzactia
        :return: erori - daca acestea exista
        '''

        if tranzactie.suma_manopera < 0:
            raise ValoarePozitiva('Suma manoperei trebuie sa fie'
                                  ' un numar pozitiv')
        if tranzactie.suma_piese < 0:
            raise ValoarePozitiva('Suma pieselor trebuie sa fie'
                                  ' un numar pozitiv')

        if len(tranzactie.ora_tranzactie) > 5:
            raise OraInvalida('Ora tranzactiei este invalida')

        zi = tranzactie.data_tranzactie[0:2]
        luna = tranzactie.data_tranzactie[3:5]
        an = tranzactie.data_tranzactie[6:10]

        if zi == '' or luna == '' or an == '':
            raise TextGol('Ziua, luna si anul nu pot fi string-uri goale')
        if len(tranzactie.data_tranzactie) > 10:
            raise DataInvalida('Data tranzactie invalida ')
        if int(luna) > 12:
            raise DataInvalida('Luna nu poate fi mai mare de 12')
        if int(zi) > 31:
            raise DataInvalida('Ziua nu poate fi mai mare de 31')
        if int(an) // 10000 != 0:
            raise DataInvalida('Anul trebuie sa fie de 4 cifre')

        if tranzactie.id_entitate == '' or tranzactie.id_masina == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
        if tranzactie.ora_tranzactie == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
        if tranzactie.id_card_client == '' or tranzactie.data_tranzactie == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
