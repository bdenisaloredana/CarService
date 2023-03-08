
def sortare(iterable, *, key=lambda x: x, reverse=False):
    '''
    Sorteaza elementele unui obiect iterabil.
    :param iterable: obiectul iterabil
    :param key: o funcție care servește drept cheie pentru compararea
    elementelor
    :param reverse: daca e True-ordoneaza elementele descrescator
                           False-ordoneaza elementele crescator
    :return: obiectul iterabil sortat
    '''
    for poz in range(len(iterable) - 1):
        for poz2 in range(poz + 1, len(iterable)):
            if reverse is False:
                if key(iterable[poz]) > key(iterable[poz2]):
                    aux = iterable[poz]
                    iterable[poz] = iterable[poz2]
                    iterable[poz2] = aux
            else:
                if key(iterable[poz]) < key(iterable[poz2]):
                    aux = iterable[poz]
                    iterable[poz] = iterable[poz2]
                    iterable[poz2] = aux
    return iterable
