from pathlib import Path

from lib.entities import StudentGrade
from lib.file_data_client import FileDataClient

TEST_DATA_PATH = Path(__file__).parent / 'students_grade_test.txt'


class TestFileDataClient:
    def test_field_names(self):
        client = FileDataClient(TEST_DATA_PATH, StudentGrade)
        assert client._field_names == ['last_name', 'subject', 'semester', 'grade']

    def test_read_at_position(self):
        client = FileDataClient(TEST_DATA_PATH, StudentGrade)
        assert client.read_at_position(47) == StudentGrade(
            last_name='two',
            subject='it',
            semester='1',
            grade='14'
        )

    def test_iter_read(self):
        client = FileDataClient(TEST_DATA_PATH, StudentGrade)
        students = [
            (StudentGrade(last_name='one', subject='math', semester='1', grade='12'), 33),
            (StudentGrade(last_name='two', subject='it', semester='1', grade='14'), 47),
        ]
        assert [student for student in client.iter_read()] == students

    def test_load_entity(self):
        client = FileDataClient(TEST_DATA_PATH, StudentGrade)
        assert client._load_entity('one,math,1,12\n') == StudentGrade(
            last_name='one',
            subject='math',
            semester='1',
            grade='12'
        )

    def test_dump_entity(self):
        client = FileDataClient(TEST_DATA_PATH, StudentGrade)

        student_grade = StudentGrade(
            last_name='one',
            subject='math',
            semester='1',
            grade='12'
        )

        assert client._dump_entity(student_grade) == 'one,math,1,12'
