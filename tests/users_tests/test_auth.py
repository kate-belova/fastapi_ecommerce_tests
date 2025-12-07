import allure
import pytest

from tests.users_tests.users_test_data import (
    invalid_auth_data,
    invalid_refresh_token,
)


@pytest.mark.users
@pytest.mark.auth
@pytest.mark.regression
class TestAuth:
    @allure.feature('Registration and authorization')
    @allure.story('Authorization')
    @allure.title('Successful authorization')
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_registered_user_successful_auth(self, registered_buyer, auth_api):
        auth_data = registered_buyer
        auth_api.get_token('access_token', auth_data)
        auth_api.assert_response_status(200)
        auth_api.assert_tokens()

    @allure.feature('Registration and authorization')
    @allure.story('Authorization')
    @allure.title('Failed authorization with invalid auth data')
    @pytest.mark.negative
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        'auth_data',
        invalid_auth_data,
        ids=[
            'unregistered_user',
            'wrong password',
            'wrong email',
            'empty fields',
        ],
    )
    def test_failed_authorization_with_invalid_auth_data(
        self, auth_api, auth_data
    ):
        auth_api.get_token('access_token', auth_data, validate=False)
        auth_api.assert_response_status(401)
        auth_api.assert_error()

    @allure.feature('Registration and authorization')
    @allure.story('Automatical refresh of access token')
    @allure.title('Successful refresh of access token')
    @pytest.mark.positive
    def test_update_access_token_success(self, authenticated_buyer):
        authenticated_buyer.get_token('refresh_token')
        authenticated_buyer.assert_response_status(200)
        authenticated_buyer.assert_tokens()

    @allure.feature('Registration and authorization')
    @allure.story('Refresh of access token')
    @allure.title('Failed refresh of access token with invalid refresh token')
    @pytest.mark.negative
    @pytest.mark.parametrize(
        'refresh_token',
        invalid_refresh_token,
        ids=[
            'empty refresh token',
            'wrong refresh token',
        ],
    )
    def test_update_access_token_with_invalid_refresh_token(
        self, authenticated_buyer, refresh_token
    ):
        authenticated_buyer.refresh_token = refresh_token
        authenticated_buyer.get_token('refresh_token')
        authenticated_buyer.assert_response_status(401)
        authenticated_buyer.assert_error()
