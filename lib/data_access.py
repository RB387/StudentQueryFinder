from dataclasses import dataclass
from typing import Protocol, List

from simio_di import Depends, Provide

from lib.entities import StudentGrade
from lib.file_data_client import FileDataClient
from lib.index import IndexProtocol
from lib.query import Query, QueryExecutorProtocol


class StudentGradeDataAccessProtocol(Protocol):
    def add(self, student_grade: StudentGrade):
        ...

    def find(self, queries: List[Query]) -> List[StudentGrade]:
        ...


@dataclass
class FileStudentGradeDataAccess(StudentGradeDataAccessProtocol):
    file_client: Depends[FileDataClient]

    index: Provide[IndexProtocol]
    query_executor: Provide[QueryExecutorProtocol]

    def __post_init__(self):
        # строим индекс при инициализации
        for student_grade, position in self.file_client.iter_read():
            self.index.add(student_grade, position)

    def add(self, student_grade: StudentGrade):
        # записали в файл
        position = self.file_client.write(student_grade)
        # обновили индекс
        self.index.add(student_grade, position)

    def find(self, queries: List[Query]) -> List[StudentGrade]:
        # Выполнили запрос, получили позиции в файле
        positions = self.query_executor.execute(queries)

        result = []

        for position in positions:
            # Ищем нужные записи в файле
            result.append(self.file_client.read_at_position(position))

        return result
