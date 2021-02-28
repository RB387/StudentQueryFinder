from dataclasses import dataclass, field

from simio_di import Depends, Provide

from cli.query import QueryInput
from cli.uploader import FileDataUploader
from lib.data_access import StudentGradeDataAccessProtocol


@dataclass
class MainActivity:
    data_access: Provide[StudentGradeDataAccessProtocol]

    uploader: Depends[FileDataUploader]
    query_input: Depends[QueryInput]

    _running: bool = field(default=True, init=False)

    def start(self):
        selector = {
            "1": self.upload,
            "2": self.find_records,
            "3": self.exit,
        }

        while self._running:
            print("Выберите действие:")
            print("1. Загрузить данные из файла")
            print("2. Найти записи")
            print("3. Выход")
            print(">> ", end="")

            user_choice = selector.get(input())

            if user_choice is None:
                print("Такого варианта ответа нет\n")
            else:
                user_choice()

    def upload(self):
        print("Начинаю загрузку")
        self.uploader.upload(self.data_access)
        print("Загрузка завершена")

    def find_records(self):
        queries = self.query_input.input()

        if not queries:
            return

        result = self.data_access.find(queries)
        print(f"Найдено: {len(result)}\n")

        for entity in result:
            print(entity)

    def exit(self):
        self._running = False
