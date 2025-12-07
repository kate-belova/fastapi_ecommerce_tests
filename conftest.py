from pathlib import Path


def pytest_configure(config):
    project_root = Path(__file__).resolve().parent
    allure_dir = project_root / 'allure-results'
    allure_dir.mkdir(exist_ok=True)
    config.option.allure_report_dir = str(allure_dir)


pytest_plugins = (
    'tests.root_tests.fixtures',
    'tests.users_tests.fixtures',
    'tests.categories_tests.fixtures',
)
