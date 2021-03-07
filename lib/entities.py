from dataclasses import dataclass, asdict
from typing import Dict, Any, Protocol


@dataclass
class DataProtocol(Protocol):
    """ Интерфейс для сущностей """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataProtocol":
        """ десериализация """
        ...

    def as_dict(self) -> Dict[str, Any]:
        """ сериализация """
        ...


@dataclass
class StudentGrade(DataProtocol):
    """ Реализация интерфейса DataProtocol для сущности студента """

    last_name: str
    subject: str
    semester: str
    grade: str

    def __str__(self):
        """ Строчное представление сущности """
        return (
            f"Last name: {self.last_name}\n"
            f"Subject: {self.subject}\n"
            f"Semester: {self.semester}\n"
            f"Grade: {self.grade}\n"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StudentGrade":
        return cls(
            last_name=data["last_name"],
            subject=data["subject"],
            semester=data["semester"],
            grade=data["grade"],
        )

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
