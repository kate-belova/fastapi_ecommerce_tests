import pytest

from endpoints import HealthAPI
from endpoints import RootAPI


@pytest.fixture
def health_api():
    return HealthAPI()


@pytest.fixture
def root_api():
    return RootAPI()
