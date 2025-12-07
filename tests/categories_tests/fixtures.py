import pytest

from endpoints import (
    GetCategoriesAPI,
    PostCategoryAPI,
    PutCategoryAPI,
    DeleteCategoryAPI,
)


@pytest.fixture
def get_categories_api():
    return GetCategoriesAPI()


@pytest.fixture
def post_category_api():
    return PostCategoryAPI()


@pytest.fixture
def put_category_api():
    return PutCategoryAPI()


@pytest.fixture
def delete_category_api():
    return DeleteCategoryAPI()
