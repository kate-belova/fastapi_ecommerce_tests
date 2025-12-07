import allure
import pytest

from tests.categories_tests.categories_test_data import categories_count


@pytest.mark.categories
@pytest.mark.crud
@pytest.mark.regression
class TestGetCategories:
    @allure.feature('Categories')
    @allure.story('Get categories')
    @allure.title('Successfully get all categories')
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.get
    def test_get_all_categories_success(self, get_categories_api):
        get_categories_api.get_categories()
        get_categories_api.assert_response_status(200)
        get_categories_api.assert_categories_count(categories_count)
        get_categories_api.assert_all_categories_active()
        get_categories_api.assert_hierarchy_ids_are_valid()
