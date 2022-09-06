from pathlib import Path
import sys

from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.runner import CallInfo
import pytest


FAILURES_FILE = Path() / "failures.txt"

@pytest.hookimpl()
def pytest_sessionstart(session: Session):
    if FAILURES_FILE:
        FAILURES_FILE.unlink()
    FAILURES_FILE.touch()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):

    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        try:
             with open(str(FAILURES_FILE), "a") as f:
                f.write(result.nodeid + "\n")
        except Exception as e:
            print(f"ERROR: {e}")
            pass
# if you have pytest-xdist installed
# this spawns the number of workers as you have cpus
# without you having to do any command line arguments
def pytest_load_initial_conftests(args):
    if "xdist" in sys.modules:  # pytest-xdist plugin
        import multiprocessing

        num = max(multiprocessing.cpu_count() / 2, 1)
        args[:] = ["-n", str(num)] + args


def test_request(request):
    print(request.session.testscollected)
    print(request.session.testsfailed)

"""
# This makes it so tests marked with incremental get skipped if one of the tests depends on # the other failing. the tests return xfail

from typing import Dict, Tuple

import pytest

# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail(f"previous test failed ({test_name})")
"""