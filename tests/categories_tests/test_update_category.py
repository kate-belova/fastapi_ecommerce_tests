import allure
import pytest

from tests.categories_tests.categories_test_data import category_data


@pytest.mark.categories
@pytest.mark.crud
@pytest.mark.regression
class TestUpdateCategory:
    @allure.feature('Categories')
    @allure.story('Update category')
    @allure.title('Try to update category by non-admin roles (seller, buyer)')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.update
    @pytest.mark.parametrize(
        'user_fixture', ['authenticated_buyer', 'authenticated_seller']
    )
    def test_update_category_by_wrong_role(
        self, auth_api, request, user_fixture, put_category_api
    ):
        auth_api = request.getfixturevalue(user_fixture)
        token = auth_api.access_token

        put_category_api.put_category(
            category_data, category_id=1, token=token
        )
        put_category_api.assert_response_status(403)
        put_category_api.assert_error()

    @allure.feature('Categories')
    @allure.story('Update category')
    @allure.title('Try to update category by non-authenticated user')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.update
    def test_update_category_by_non_authenticated_user(self, put_category_api):
        put_category_api.put_category(category_data, category_id=1)
        put_category_api.assert_response_status(401)
        put_category_api.assert_error()

    @allure.feature('Categories')
    @allure.story('Update category')
    @allure.title('Try to update category without providing its id')
    @pytest.mark.negative
    @pytest.mark.update
    def test_update_category_without_its_id(self, put_category_api):
        put_category_api.put_category(category_data)
        put_category_api.assert_response_status(405)
