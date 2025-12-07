import allure
import pytest


@pytest.mark.categories
@pytest.mark.crud
@pytest.mark.regression
class TestDeleteCategory:
    @allure.feature('Categories')
    @allure.story('Delete category')
    @allure.title('Try to delete category by non-admin roles (seller, buyer)')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.delete
    @pytest.mark.parametrize(
        'user_fixture', ['authenticated_buyer', 'authenticated_seller']
    )
    def test_delete_category_by_wrong_role(
        self, auth_api, request, user_fixture, delete_category_api
    ):
        auth_api = request.getfixturevalue(user_fixture)
        token = auth_api.access_token

        delete_category_api.delete_category(category_id=1, token=token)
        delete_category_api.assert_response_status(403)
        delete_category_api.assert_error()

    @allure.feature('Categories')
    @allure.story('Delete category')
    @allure.title('Try to delete category by non-authenticated user')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.delete
    def test_delete_category_by_non_authenticated_user(
        self, delete_category_api
    ):
        delete_category_api.delete_category(category_id=1)
        delete_category_api.assert_response_status(401)
        delete_category_api.assert_error()

    @allure.feature('Categories')
    @allure.story('Delete category')
    @allure.title('Try to delete category without providing its id')
    @pytest.mark.negative
    @pytest.mark.delete
    def test_delete_category_without_its_id(self, delete_category_api):
        delete_category_api.delete_category()
        delete_category_api.assert_response_status(405)
