import allure
import pytest

from tests.users_tests.users_test_data import (
    valid_user_data,
    invalid_user_data,
)


@pytest.mark.users
class TestUserRegistration:
    @allure.feature('Registration and authorization')
    @allure.story('Registration')
    @allure.title('Successful registration')
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize(
        'user_data',
        valid_user_data,
        ids=[
            'min pass length and default role (buyer)',
            'seller role',
            'buyer role',
        ],
    )
    def test_register_new_user_success(self, users_api, user_data):
        users_api.register_new_user(user_data)

        users_api.assert_response_status(201)
        users_api.assert_response_data(user_data)
        users_api.assert_new_user_in_db()

    @allure.feature('Registration and authorization')
    @allure.story('Registration')
    @allure.title('Unsuccessful registration with invalid data')
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.parametrize(
        'user_data',
        invalid_user_data,
        ids=[
            'data with empty fields',
            'email without @',
            'email without dot and domen',
            'email without domen',
            'empty password',
            'invalid password (too short)',
            'empty role',
            'invalid role (not buyer or seller)',
        ],
    )
    def test_register_new_user_with_invalid_data(self, users_api, user_data):
        users_api.register_new_user(user_data, validate=False)
        users_api.assert_response_status(422)
