import allure
import pytest

from tests.categories_tests.categories_test_data import category_data


@pytest.mark.categories
@pytest.mark.crud
@pytest.mark.regression
class TestPostCategory:

    @allure.feature('Categories')
    @allure.story('Create category')
    @allure.title(
        'Category creation: Access denied for non-admin roles '
        '(seller, buyer)'
    )
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.create
    @pytest.mark.parametrize(
        'user_fixture', ['authenticated_buyer', 'authenticated_seller']
    )
    def test_create_new_category_by_wrong_role(
        self, auth_api, request, user_fixture, post_category_api
    ):
        auth_api = request.getfixturevalue(user_fixture)
        token = auth_api.access_token

        post_category_api.post_category(category_data, token)
        post_category_api.assert_response_status(403)
        post_category_api.assert_error()

    @allure.feature('Categories')
    @allure.story('Create category')
    @allure.title(
        'Category creation: Access denied for non-authenticated user'
    )
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.create
    def test_create_new_category_by_non_authenticated_user(
        self, post_category_api
    ):
        post_category_api.post_category(category_data)
        post_category_api.assert_response_status(401)
        post_category_api.assert_error()
