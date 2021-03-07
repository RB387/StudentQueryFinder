from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

from lib.index import InvertedIndex
from lib.query import IndexQueryExecutor


INDEX = {
    'subject': {
        'math': {1, 3},
        'it': {2},
    },
    'last_name': {
        'one': {1},
        'two': {2},
        'three': {3},
    },
    'grade': {
        '14': {1, 2},
        '15': {3},
    },
    'semester': {
        '1': {1, 2, 3},
    },
}


@pytest.fixture
def index_query_executor():
    index = InvertedIndex()
    index._index = INDEX
    index.add = MagicMock()

    return IndexQueryExecutor(index=index)


@contextmanager
def does_not_raise():
    yield None
