from typing import List, Dict

import pytest

from pepino.exceptions import CucumberTableException
from pepino.gherkin.data import GherkinDataTable


def create_table(sequence: List[List[str]]) -> GherkinDataTable:
    data = {
        "location": {
            "line": 0,
            "column": 0
        },
        "rows": [
            {
                "location": {
                    "line": 0,
                    "column": 0
                },
                "cells": [
                    {
                        "location": {
                            "line": 0,
                            "column": 0
                        },
                        "value": value
                    }
                    for value in row
                ]

            }
            for row in sequence
        ]
    }
    return GherkinDataTable(data)


class User:

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = int(age)


class Numbers:

    def __init__(self, first, second):
        self.first = int(first)
        self.second = int(second)


def test_datatable_rows():
    table = create_table([["first_name", "last_name", "age"], ["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    assert table.row(0) == ["first_name", "last_name", "age"]
    assert table.row(1) == ["joe", "bloggs", "18"]
    assert table.row(2) == ["joanne", "bloggs", "20"]


def test_datatable_row_execption():
    table = create_table([["first_name", "last_name", "age"], ["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    with pytest.raises(CucumberTableException) as excinfo:
        table.row(5)
    assert str(excinfo.value) == "No row for index 5 failed at 0:0"


def test_datatable_columns():
    table = create_table([["first_name", "last_name", "age"], ["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    assert table.column(0) == ["first_name", "joe", "joanne"]
    assert table.column(1) == ["last_name", "bloggs", "bloggs"]
    assert table.column(2) == ["age", "18", "20"]
    assert table.column("first_name") == ["joe", "joanne"]
    assert table.column("last_name") == ["bloggs", "bloggs"]
    assert table.column("age") == ["18", "20"]


def test_datatable_column_invalid_number():
    table = create_table([["first_name", "last_name", "age"], ["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    with pytest.raises(CucumberTableException) as excinfo:
        table.column(5)
    assert str(excinfo.value) == "No column for index 5 failed at 0:0"


def test_datatable_column_invalid_column_name():
    table = create_table([["first_name", "last_name", "age"], ["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    with pytest.raises(CucumberTableException) as excinfo:
        table.column("spam")
    assert str(excinfo.value) == "No column called spam failed at 0:0"


def test_datatable_convert_column_dict_list_str():
    table = create_table([["first_name", "last_name", "age"], ["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    data = table.convert(True, Dict[str, List[str]])
    assert data["first_name"] == ["joe", "joanne"]
    assert data["last_name"] == ["bloggs", "bloggs"]
    assert data["age"] == ["18", "20"]


def test_datatable_convert_column_dict_list_int():
    table = create_table([["apples", "bannanas", "lemons"], ["6", "7", "18"], ["4", "9", "20"]])
    data = table.convert(True, Dict[str, List[int]])
    assert data["apples"] == [6, 4]
    assert data["bannanas"] == [7, 9]
    assert data["lemons"] == [18, 20]


def test_datatable_convert_column_dict_int():
    table = create_table([["apples", "bannanas", "lemons"], ["6", "7", "18"], ["4", "9", "20"]])
    data = table.convert(True, Dict[str, int])
    assert data["apples"] == 6
    assert data["bannanas"] == 7
    assert data["lemons"] == 18


def test_datatable_convert_column_list_dict():
    table = create_table([["apples", "bannanas", "lemons"], ["6", "7", "18"], ["4", "9", "20"]])
    data = table.convert(True, List[Dict[str, List[int]]])
    assert data[0] == {"apples": [6, 4]}
    assert data[1] == {"bannanas": [7, 9]}
    assert data[2] == {"lemons": [18, 20]}


def test_datatable_convert_column_list_list():
    table = create_table([["apples", "bannanas", "lemons"], ["6", "7", "18"], ["4", "9", "20"]])
    data = table.convert(True, List[List[str]])
    assert data[0] == ["apples", "6", "4"]
    assert data[1] == ["bannanas", "7", "9"]
    assert data[2] == ["lemons", "18", "20"]


def test_datatable_convert_column_single_str():
    table = create_table([["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    data = table.convert(True, str)
    assert data == "joe"


def test_datatable_convert_column_single_numbers():
    table = create_table([["9", "8", "18"], ["1", "3", "20"]])
    data = table.convert(True, Numbers)
    assert data.first == 9
    assert data.second == 1


def test_datatable_convert_row_list_list():
    table = create_table([["apples", "6", "4"], ["bannanas", "7", "9"], ["lemons", "18", "20"]])
    data = table.convert(False, List[List[str]])
    assert data[0] == ["apples", "6", "4"]
    assert data[1] == ["bannanas", "7", "9"]
    assert data[2] == ["lemons", "18", "20"]


def test_datatable_convert_row_dict_list_int():
    table = create_table([["apples", "6", "4"], ["bannanas", "7", "9"], ["lemons", "18", "20"]])
    data = table.convert(False, Dict[str, List[int]])
    assert data["apples"] == [6, 4]
    assert data["bannanas"] == [7, 9]
    assert data["lemons"] == [18, 20]


def test_datatable_convert_row_dict_list_dict_list_int():
    table = create_table([["apples", "6", "4"], ["bannanas", "7", "9"], ["lemons", "18", "20"]])
    data = table.convert(False, List[Dict[str, List[int]]])
    assert data[0] == {"apples": [6, 4]}
    assert data[1] == {"bannanas": [7, 9]}
    assert data[2] == {"lemons": [18, 20]}


def test_datatable_convert_row_dict_numbers():
    table = create_table([["apples", "6", "4"], ["bannanas", "7", "9"], ["lemons", "18", "20"]])
    data = table.convert(False, Dict[str, Numbers])
    assert data["apples"].first == 6
    assert data["apples"].second == 4
    assert data["bannanas"].first == 7
    assert data["bannanas"].second == 9
    assert data["lemons"].first == 18
    assert data["lemons"].second == 20


def test_datatable_convert_row_list_users():
    table = create_table([["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    data = table.convert(False, List[User])
    assert data[0].first_name == "joe"
    assert data[0].last_name == "bloggs"
    assert data[0].age == 18
    assert data[1].first_name == "joanne"
    assert data[1].last_name == "bloggs"
    assert data[1].age == 20


def test_datatable_convert_row_single_str():
    table = create_table([["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    data = table.convert(False, str)
    assert data == "joe"


def test_datatable_convert_row_single_user():
    table = create_table([["joe", "bloggs", "18"], ["joanne", "bloggs", "20"]])
    data = table.convert(False, User)
    assert data.first_name == "joe"
    assert data.last_name == "bloggs"
    assert data.age == 18
