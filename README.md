# Pepino Behaviour Driven Dvelopment

![build status](https://github.com/patrickguk/pepino/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/patrickguk/pepino/branch/main/graph/badge.svg?token=6L0FUJOWSX)](https://codecov.io/gh/patrickguk/pepino)

Pepino is a Typed Object Orientated BDD that allows you to incorporate BDD features easily.

 Creating steps
====

To specify a test. a step just fo:

```python

from pepino.steps import given, when

@given('perform my step')
def my_step():
    ...

# Step with arguments

@when("I subtract <second> from <first> I get <third>")
def step_with_aguments(first: int, second: int, third: int):
    assert second - first == third
```

By using python 3 typing pepino is able to work out what values are susposed to be before injecting them into the function

### Working with Tables.

If you have a table in you featue it can be converted to a more usable python structure. If you had the structure below:

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| value 1  | value 2  | value3   |
| value 4  | value 5  | value 6  |

Then it can be used as follows:

```python
from typing import Dict, List
from pepino.steps import when
from pepino.data import DataTable

@when("I have the following DataTable:")
def test_datatable(table: DataTable):
    data = table.convert(True,  Dict[str,List[str]])
    # data is now {'Header 1' : ['value 1'', 'value 4'], ...}

```

If a step contains a DataTable it will get added to the call provided there is an argument which specifies the DataTbale type. when calling convert, it takes two arguments. The first being wether to treat the table as a list of columns (default True) or a list of rows. the second is the desired return type