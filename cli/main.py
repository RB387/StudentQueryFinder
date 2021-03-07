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
        self._running = True

        selector = {
            "1": self._upload,
            "2": self._find_records,
            "3": self._exit,
        }

        while self._running:
            print("Choose action:")
            print("1. Upload data from file")
            print("2. Find records")
            print("3. Exit")
            print(">> ", end="")

            user_choice = selector.get(input())

            if user_choice is None:
                print("No such option\n")
            else:
                user_choice()

    def _upload(self):
        print("Start uploading")

        self.uploader.upload(self.data_access)

        print("Finished uploading")

    def _find_records(self):
        queries = self.query_input.input()

        if not queries:
            return

        result = self.data_access.find(queries)
        print(f"Found: {len(result)}\n")

        for entity in result:
            print(entity)

    def _exit(self):
        self._running = False
