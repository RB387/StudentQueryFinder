import pytest

from lib.query import Query, LogicalOperator
from tests.test_lib.conftest import does_not_raise


@pytest.mark.parametrize(
    'queries, expected_result, expected_exception',
    (
        (
            [
                Query(
                    field_name='semester',
                    value='1',
                    operator=LogicalOperator.OR,
                ),
            ],
            {1, 2, 3},
            does_not_raise(),
        ),
        (
            [
                Query(
                    field_name='last_name',
                    value='one',
                    operator=LogicalOperator.OR,
                ),
                Query(
                    field_name='last_name',
                    value='two',
                    operator=LogicalOperator.OR,
                ),
            ],
            {1, 2},
            does_not_raise(),
        ),
        (
            [
                Query(
                    field_name='last_name',
                    value='one',
                    operator=LogicalOperator.OR,
                ),
                Query(
                    field_name='grade',
                    value='14',
                    operator=LogicalOperator.AND,
                ),
            ],
            {1},
            does_not_raise(),
        ),
        (
            [
                Query(
                    field_name='last_name',
                    value='one',
                    operator=LogicalOperator.OR,
                ),
                Query(
                    field_name='grade',
                    value='15',
                    operator=LogicalOperator.AND,
                ),
            ],
            set(),
            does_not_raise(),
        ),
        (
            [
                Query(
                    field_name='last_name',
                    value='one',
                    operator=LogicalOperator.OR,
                ),
                Query(
                    field_name='grade',
                    value='15',
                    operator=LogicalOperator.AND,
                ),
                Query(
                    field_name='last_name',
                    value='two',
                    operator=LogicalOperator.OR,
                ),
            ],
            {2},
            does_not_raise(),
        ),
        (
            [
                Query(
                    field_name='last_name',
                    value='one',
                    operator='UNKNOWN LOGICAL OPERATOR',
                )
            ],
            None,
            pytest.raises(ValueError),
        ),
    )
)
def test_index_query(index_query_executor, queries, expected_result, expected_exception):
    with expected_exception:
        result = index_query_executor.execute(queries)
        assert result == expected_result
