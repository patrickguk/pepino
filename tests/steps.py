from typing import List, Dict
from pepino import given, when, then, world, DataTable
from math import factorial


class Coordinate:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate at {self.x}:{self.y}"


@given("This is a test")
def is_a_test():
    assert True


@given("I have the number <number>")
def have_the_number(number: int):
    world.number = number


@when("I compute its factorial")
def compute_its_factorial():
    world.number = factorial(world.number)


@then("I see the number <expected>")
def check_number(expected: int):
    assert world.number == expected, f"Got {world.number} expected {expected}"


@given("there are <expected> cucumbers")
def there_are_cucumbers(expected: int):
    world.cucumbers = expected


@when("I eat <amount> cucumbers")
def eat_cucumbers(amount: int):
    world.cucumbers -= amount


@then("I should have <total> cucumbers")
def check_cucumbers_amount(total: int):
    assert world.cucumbers == total, f"Got {world.cucumbers} expected {total}"


class DatatablesTest:

    def __init__(self):
        self.table: DataTable = None

    @given("I have the following:")
    def given_a_table(self, table: DataTable):
        self.table = table

    @then("I can convert it to a horizontal dictonary of lists")
    def check_horizontal_dict(self):
        convert = self.table.convert(True, Dict[str, List[int]])
        header = [v.value for v in self.table.rows[0].cells]
        assert list(convert.keys()) == header, f"{list(convert.keys())} is not {header}"

    @then("I can convert it to a horizontal dictonary of coordinates")
    def check_horizontal_dict_coordinate(self):
        self.table.convert(True, Dict[str, Coordinate])

    @then("I can convert it to a horizontal dictonary of ints")
    def check_horizontal_dict_ints(self):
        convert = self.table.convert(True, Dict[str, int])
        header = [v.value for v in self.table.rows[0].cells]
        assert list(convert.keys()) == header, f"{list(convert.keys())} is not {header}"
        values = [int(v.value) for v in self.table.rows[1].cells]
        assert (
            list(convert.values()) == values
        ), f"{list(convert.values())} is not {values}"

    @then("I can convert it to a horizontal lists of dictonarys")
    def check_horizontal_list_dicts(self):
        self.table.convert(True, List[Dict[str, List[int]]])

    @then("I can convert it to a horizontal lists of lists")
    def check_horizontal_list_list(self):
        self.table.convert(True, List[List[str]])

    @then("I can convert it to a vertical dictonary of lists")
    def check_vertical_dict(self):
        convert = self.table.convert(False, Dict[str, List[int]])
        header = self.table.column(0)
        assert list(convert.keys()) == header, f"{list(convert.keys())} is not {header}"

    @then("I can convert it to a vertical dictonary of coordinates")
    def check_vertical_dict_coordinate(self):
        self.table.convert(False, Dict[str, Coordinate])

    @then("I can convert it to to vertical dictonary of ints")
    def check_vertical_dict_ints(self):
        convert = self.table.convert(False, Dict[str, int])
        header = self.table.column(0)
        assert list(convert.keys()) == header, f"{list(convert.keys())} is not {header}"
        values = [int(v) for v in self.table.column(1)]
        assert (
            list(convert.values()) == values
        ), f"{list(convert.values())} is not {values}"

    @then("I can convert it to a vertical lists of dictonarys")
    def check_vertical_list_dicts(self):
        self.table.convert(False, List[Dict[str, List[int]]])

    @then("I can convert it to a vertical lists of lists")
    def check_vertical_list_lists(self):
        self.table.convert(False, List[List[str]])


class MarkupTest:

    @given("I have the following markup:")
    def have_the_following_markup(self, markup: str):
        self.markup = markup

    @then("check markup length is <markup_length>")
    def check_markup_length(self, markup_length: int):
        assert markup_length == len(
            self.markup
        ), f"Got {len(self.markup)} Expected {markup_length}"
