from pepino.enums import Hook
import sys
from typing import Optional
from pepino import hooks
from pepino.gherkin.definitions import GherkinFeature, GherkinScenario, GherkinRule, Step
from pepino.results import StepResult, Result
from pepino.registry import registry

import pytest
from _pytest.capture import CaptureManager
from _pytest.terminal import TerminalReporter
from _pytest._code import ExceptionInfo


@pytest.mark.trylast
def pytest_configure(config):
    reporter = config.pluginmanager.getplugin("terminalreporter")
    capture = config.pluginmanager.getplugin("capturemanager")
    if config.option.verbose and isinstance(reporter, TerminalReporter):
        GherkinReporter(reporter=reporter, capture_manager=capture)
    registry.load_from_path("tests/.*steps.py$")


def pytest_collect_file(path, parent):
    if path.ext == ".feature":
        return FeatureCollector.from_parent(parent, fspath=path)


class GherkinReporter:

    def __init__(self, reporter: TerminalReporter, capture_manager: CaptureManager) -> None:
        self._reporter = reporter
        self._capture_manager = capture_manager
        registry.add_hook(Hook.pre_step, self.log_pre_step)
        registry.add_hook(Hook.post_step, self.log_post_step)

    def log_pre_step(self, step: Step):
        self._capture_manager.suspend()
        print(f"{step.keyword} {step.text}", end="\r")
        self._capture_manager.resume()

    def log_post_step(self, step_result: StepResult):
        self._capture_manager.suspend()
        result = "OK" if step_result.result == Result.PASSED else "FAILED"
        print(f"{step_result.step.keyword} {step_result.step.text} [{result}] ({step_result.duration.microseconds:.2f})")
        self._capture_manager.resume()


class FeatureCollector(pytest.Collector):

    def __init__(self, parent, fspath) -> None:
        super().__init__(fspath.basename, parent=parent)
        self.fspath = fspath

    def collect(self):
        with self.fspath.open() as fp:
            feature = GherkinFeature.from_string(fp.read())
            for rule in feature.rules:
                for scenario in rule.scenarios:
                    yield ScenarioItem.from_parent(self, feature=feature, scenario=scenario, rule=rule)
            for scenario in feature.scenarios:
                yield ScenarioItem.from_parent(self, feature=feature, scenario=scenario)


class ScenarioItem(pytest.Item):

    def __init__(self, parent: FeatureCollector, feature: GherkinFeature, scenario: GherkinScenario, rule: Optional[GherkinRule] = None) -> None:
        if rule:
            name = f"{feature.name}/{rule.name}/{scenario.name}"
            nodeid = f"{feature.name}/{rule.name}::{scenario.name}"
        else:
            name = f"{feature.name}/{scenario.name}"
            nodeid = f"{feature.name}::{scenario.name}"
        super(ScenarioItem, self).__init__(name, parent, nodeid=nodeid)
        self.feature = feature
        self.scenario = scenario
        self.rule = rule

    def runtest(self):
        if self.feature.background:
            result = self.feature.background.execute()
            if result.exc_info:
                raise PepinoException(result.exc_info)
        result = self.scenario.execute()
        if result.exc_info:
            raise PepinoException(result.exc_info)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, PepinoException):
            return self._repr_failure_py(ExceptionInfo.from_exc_info(excinfo.value.exc_info), "short")
        return ""

    def reportinfo(self):
        if self.rule:
            return f"{self.feature.name}::{self.rule.name}", self.scenario.line, "Scenario:: %s" % self.scenario.name
        return f"{self.feature.name}", self.scenario.line, "Scenario: %s" % self.scenario.name


class PepinoException(Exception):

    def __init__(self, exc_info):
        super(PepinoException, self).__init__()
        self.exc_info = exc_info
