from typing import List

from more_itertools import chunked

from lib.query import Query, LogicalOperator

EXIT_VALUE = "1"


class QueryInput:
    def input(self) -> List[Query]:
        while True:
            print("Введите запрос в формате: поле1 значение [логический оператор] поле2 значение")
            print("Допустимые логические операторы: and, or")
            print("Пример запроса: subject Информатика and grade 4")
            print(f"Введите {EXIT_VALUE} для выхода")
            print(">> ", end="")

            user_input = input()
            if user_input == EXIT_VALUE:
                return []

            queries = self._parse_input(user_input)

            return queries

    def _parse_input(self, user_input: str) -> List[Query]:
        # Первый запрос всегда имеет логический оператор ИЛИ
        str_query_parts = [LogicalOperator.OR.value, *user_input.split()]
        queries = []

        if len(str_query_parts) < 3:
            print("Некорректный запрос")
            return self.input()

        try:
            for operator, field_name, value in chunked(str_query_parts, 3):
                try:
                    operator = LogicalOperator(operator)
                except ValueError:
                    print(f"Некорректный логический оператор: {operator}")
                    return self.input()

                queries.append(Query(field_name=field_name, value=value, operator=operator))
        except ValueError:
            print("Некорректный запрос")
            return self.input()

        return queries
