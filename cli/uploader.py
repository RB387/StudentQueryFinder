from dataclasses import dataclass

from simio_di import Depends

from lib.data_access import StudentGradeDataAccessProtocol, StudentGrade
from lib.file_data_client import FileDataClient


class NewDataFileClient(FileDataClient):
    def clear(self):
        with open(self.file_path, "w+") as file:
            header = self.delimiter.join(self._field_names)
            file.write(header)
            file.write(self.new_line)


@dataclass
class FileDataUploader:
    """ Загрузчик данных из загручного файла """
    source_data_client: Depends[NewDataFileClient]  # type: NewDataFileClient[StudentGrade]

    def upload(self, target: StudentGradeDataAccessProtocol):
        for student_grade, _ in self.source_data_client.iter_read():
            # Прочитали из загрузочного, загрузили в информационный
            target.add(student_grade)

        # чистим загрузочный файл
        self.source_data_client.clear()
