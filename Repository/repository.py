from typing import Protocol, Type, Union, Optional, List

from Domain.entitate import Entitate


class Repository(Protocol):
    def create(self, entitate: Entitate) -> None:
        ...

    def read(self, id_entitate=None) \
            -> Type[Union[Optional[Entitate], List[Entitate]]]:
        ...

    def update(self, entitate: Entitate) -> None:
        ...

    def delete(self, id_entitate: str) -> None:
        ...
