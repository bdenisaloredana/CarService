from Domain.card_client import CardClient
from Repository.exceptii import TextGol, DataInvalida


class ValidareCardClient:

    def valideaza(self, card_client: CardClient) -> None:
        '''
        Valideaza un card de client.
        :param card_client: cardul de client
        :return: erori- daca acestea exista
        '''

        zi_n = int(card_client.data_nastere[0:2])
        luna_n = int(card_client.data_nastere[3:5])
        an_n = int(card_client.data_nastere[6:10])
        if len(card_client.data_nastere) > 10:
            raise DataInvalida('Data nasterii invalida')

        if luna_n > 12:
            raise DataInvalida('Luna nu poate fi mai mare de 12')
        if zi_n > 31:
            raise DataInvalida('Ziua nu poate fi mai mare de 31')
        if an_n // 10000 != 0:
            raise DataInvalida('Anul trebuie sa fie de 4 cifre')

        zi_i = int(card_client.data_inregistrare[0:2])
        luna_i = int(card_client.data_inregistrare[3:5])
        an_i = int(card_client.data_inregistrare[6:10])
        if len(card_client.data_inregistrare) > 10:
            raise DataInvalida('Data inregistrarii invalida')
        if luna_i > 12:
            raise DataInvalida('Luna nu poate fi mai mare de 12')
        if zi_i > 31:
            raise DataInvalida('Ziua nu poate fi mai mare de 31')
        if an_i // 10000 != 0:
            raise DataInvalida('Anul trebuie sa fie de 4 cifre')

        if card_client.id_entitate == '' or card_client.data_nastere == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')

        if card_client.data_inregistrare == '' or card_client.nume == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
        if card_client.prenume == '' or card_client.cnp == '':
            raise TextGol('Niciunul dinte campuri nu poate fi gol')
