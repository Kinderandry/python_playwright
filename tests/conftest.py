import pytest


def pytest_addoption(parser):
    parser.addoption('--base-url', action='store')


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption('--base-url')
