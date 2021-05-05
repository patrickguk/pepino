from pepino import when
from pepino.results import Result
from pepino.exceptions import UnknownStepException, CucumberStepException
from pepino.gherkin.definitions import GherkinStep


@when('Step does exist')
def step_does_exist():
    ...


@when('Step causes error')
def step_cause_error():
    raise Exception('broke')


@when("Step expects args error")
def step_expects_args_error(a, b, c):
    ...


@when("Step adds <first> to <second> i get the result <result> which is awesome")
def step_can_convert_args(first: int, second: int, result: int):
    assert first + second == result


def test_step_does_not_exist():
    step = GherkinStep({'location': {'line': 0, 'column': 0}, 'keyword': 'Given', 'text': 'Step does not exist'})
    result = step.execute()
    assert result.result == Result.FAILED
    assert isinstance(result.exc_info[1], UnknownStepException)


def test_step_does_exist():
    step = GherkinStep({'location': {'line': 0, 'column': 0}, 'keyword': 'Given', 'text': 'Step does exist'})
    result = step.execute()
    assert result.result == Result.PASSED


def test_step_causes_error():
    step = GherkinStep({'location': {'line': 0, 'column': 0}, 'keyword': 'Given', 'text': 'Step causes error'})
    result = step.execute()
    assert result.result == Result.FAILED
    assert isinstance(result.exc_info[1], CucumberStepException)


def test_step_expects_args_error():
    step = GherkinStep({'location': {'line': 0, 'column': 0}, 'keyword': 'Given', 'text': 'Step expects args error'})
    result = step.execute()
    assert result.result == Result.FAILED
    assert isinstance(result.exc_info[1], CucumberStepException)


def test_step_can_convert_args():
    step = GherkinStep({'location': {'line': 0, 'column': 0}, 'keyword': 'Given', 'text': 'Step adds 1 to 2 i get the result 3 which is awesome'})
    result = step.execute()
    assert result.result == Result.PASSED
