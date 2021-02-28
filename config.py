import os
from pathlib import Path

from cli.uploader import NewDataFileClient
from lib.data_access import StudentGradeDataAccessProtocol, FileStudentGradeDataAccess
from lib.entities import StudentGrade
from lib.file_data_client import FileDataClient
from lib.index import IndexProtocol, InvertedIndex
from lib.query import QueryExecutorProtocol, IndexQueryExecutor


def get_config():
    return {
        IndexProtocol: InvertedIndex,
        QueryExecutorProtocol: IndexQueryExecutor,
        StudentGradeDataAccessProtocol: FileStudentGradeDataAccess,
        FileDataClient: {
            "file_path": os.path.join(Path(__file__).parent, "main_students.txt"),
            "entity_type": StudentGrade,
        },
        NewDataFileClient: {
            "file_path": os.path.join(Path(__file__).parent, "upload_students.txt"),
            "entity_type": StudentGrade,
        },
    }
