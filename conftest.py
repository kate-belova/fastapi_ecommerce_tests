from pathlib import Path

import pytest

from endpoints import HealthAPI
from endpoints import RootAPI


def pytest_configure(config):
    project_root = Path(__file__).resolve().parent
    allure_dir = project_root / 'allure-results'
    allure_dir.mkdir(exist_ok=True)
    config.option.allure_report_dir = str(allure_dir)


@pytest.fixture
def health_api():
    return HealthAPI()


@pytest.fixture
def root_api():
    return RootAPI()
