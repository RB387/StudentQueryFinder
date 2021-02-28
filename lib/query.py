from dataclasses import dataclass
from enum import Enum
from typing import List, Collection

from simio_di import Provide

from lib.index import IndexProtocol, RecordNotFound


class LogicalOperator(Enum):
    AND = "and"
    OR = "or"


@dataclass
class Query:
    field_name: str
    value: str
    operator: LogicalOperator


@dataclass
class QueryExecutorProtocol:
    """ Интерфейс для исполнителя запросов """
    def execute(self, query: List[Query]) -> Collection[int]:
        ...


@dataclass
class IndexQueryExecutor(QueryExecutorProtocol):
    """ Исполнитель запросов, использующий индекс """
    index: Provide[IndexProtocol]

    def execute(self, queries: List[Query]) -> Collection[int]:
        result = set()

        for query in queries:
            try:
                positions = self.index.find(query.field_name, query.value)
            except RecordNotFound:
                positions = set()

            if query.operator is LogicalOperator.AND:
                # Если оператор И, то делаем пересечение множеств
                result = result.intersection(positions)
            elif query.operator is LogicalOperator.OR:
                # Если оператор ИЛИ, то объединение
                result = result.union(positions)
            else:
                raise ValueError(f"Unexpected logical operator: {query.operator}")

        return result
