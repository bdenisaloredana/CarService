from datetime import datetime
from Domain.masina import Masina
from Repository.exceptii import TextGol, ValoarePozitiva,\
    DataInvalida, GarantieInvalida


class ValidareMasina:

    def valideaza(self, masina: Masina) -> None:
        '''
        Valideaza o masina.
        :param masina: masina
        :return: erori- daca acestea exista
        '''

        garantie = ['da', 'nu']
        if float(masina.nr_km) < 0:
            raise ValoarePozitiva('Numarul de km trebuie sa fie'
                                  ' strict pozitiv')
        if masina.in_garantie not in garantie:
            raise GarantieInvalida('In garantie trebuie sa aiba '
                                   'valoarea da sau nu')
        if int(masina.an_achizitie) <= 0:
            raise ValoarePozitiva('Anul achizitiei trebuie sa fie'
                                  ' strict pozitiv')
        if int(masina.an_achizitie) // 10000 != 0:
            raise DataInvalida('Anul trebuie sa fie de 4 cifre')
        if masina.id_entitate == '' or masina.in_garantie == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
        if masina.model == '' or masina.an_achizitie == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
        an = datetime.now().year
        if int(masina.an_achizitie) > an:
            raise DataInvalida(f'Anul nu poate fi mai mare decat {an}')
