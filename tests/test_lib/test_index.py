import pytest

from lib.entities import StudentGrade
from lib.index import InvertedIndex, RecordNotFound
from tests.test_lib.conftest import does_not_raise


class TestInvertedIndex:
    @pytest.mark.parametrize(
        'entities, expected_index',
        (
            (
                [
                    (
                        StudentGrade(
                            last_name='one',
                            subject='math',
                            semester='1',
                            grade='14'
                        ),
                        1,
                    ),
                ],
                {
                    'last_name': {'one': {1}},
                    'semester': {'1': {1}},
                    'subject': {'math': {1}},
                    'grade': {'14': {1}}
                },
            ),
            (
                    [
                        (
                                StudentGrade(
                                    last_name='one',
                                    subject='math',
                                    semester='1',
                                    grade='14'
                                ),
                                1,
                        ),
                        (
                                StudentGrade(
                                    last_name='two',
                                    subject='math',
                                    semester='2',
                                    grade='14'
                                ),
                                2,
                        ),
                    ],
                    {
                        'last_name': {'one': {1}, 'two': {2}},
                        'semester': {'1': {1}, '2': {2}},
                        'subject': {'math': {1, 2}},
                        'grade': {'14': {1, 2}}
                    },
            ),
        )
    )
    def test_add(self, entities, expected_index):
        index = InvertedIndex()

        for entity, position in entities:
            index.add(entity, position)

        index = dict(index._index)
        for key, value in index.items():
            index[key] = dict(index[key])

        assert index == expected_index

    @pytest.mark.parametrize(
        'index, field, value, expected_result, expected_exception',
        (
            (
                {'last_name': {'one': {1, 2}}},
                'last_name',
                'one',
                {1, 2},
                does_not_raise(),
            ),
            (
                {'last_name': {'one': {1, 2}}},
                'unknown_field',
                'one',
                None,
                pytest.raises(RecordNotFound),
            ),
            (
                {'last_name': {'one': {1, 2}}},
                'last_name',
                'unknown_value',
                None,
                pytest.raises(RecordNotFound),
            ),
        )
    )
    def test_find(self, index, field, value, expected_result, expected_exception):
        inverted_index = InvertedIndex()
        inverted_index._index = index

        with expected_exception:
            result = inverted_index.find(field, value)
            assert result == expected_result
