from collections import defaultdict
from dataclasses import dataclass, field
from functools import partial
from typing import Dict, Set, Protocol

from lib.entities import DataProtocol

IndexData = Dict[str, Dict[str, Set[int]]]


class RecordNotFound(Exception):
    ...


class IndexProtocol(Protocol):
    """ Интерфейс для индекса """
    def add(self, entity: DataProtocol, position: int):
        ...

    def find(self, field_name: str, value: str) -> Set[int]:
        ...


def create_empty_index() -> IndexData:
    """ Фабрика со структурой данный индекса """
    default_dict_with_set = partial(defaultdict, set)
    return defaultdict(default_dict_with_set)


@dataclass
class InvertedIndex(IndexProtocol):
    """ Реализация индекса по принципу инвертированного списка """
    _index: IndexData = field(default_factory=create_empty_index, init=False)

    def add(self, entity: DataProtocol, position: int):
        for key, value in entity.as_dict().items():
            # Приводим значение к нижнему регистру
            # для регистро независимого поиска
            self._index[key][value.lower()].add(position)

    def find(self, field_name: str, value: str) -> Set[int]:
        """ Поиск в индексе по полю и значение. Возвращает множество позиций """
        field_values = self._index.get(field_name)
        if field_values is None:
            # Такого поля не существует
            raise RecordNotFound(f"Field {field_name} not found")

        positions = field_values.get(value.lower())
        if positions is None:
            # Таких значений для поля не найдено
            raise RecordNotFound(f"Value {value} of field {field_name} not found")

        return positions
