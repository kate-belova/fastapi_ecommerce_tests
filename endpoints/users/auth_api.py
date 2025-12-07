import allure
import pytest
import requests

from endpoints import UsersAPI
from schemas import (
    AuthRequestSchema,
    AuthResponseSchema,
    RefreshTokenResponseSchema,
)


class AuthAPI(UsersAPI):
    def __init__(self):
        super().__init__()

        self.access_token_url = None
        self.refresh_token_url = None

        self.access_token = None
        self.refresh_token = None
        self.token_type = 'bearer'

    @allure.step('Send POST request to get {token}')
    def get_token(self, token, auth_data=None, validate=True):
        if token == 'access_token':
            self.access_token_url = self.url + 'token'
            payload = auth_data
            if validate and auth_data:
                payload = AuthRequestSchema(**auth_data).model_dump()
            self.response = requests.post(
                url=self.access_token_url, data=payload
            )

        else:
            self.refresh_token_url = (
                self.url + f'refresh-token?refresh_token={self.refresh_token}'
            )
            self.response = requests.post(url=self.refresh_token_url)

        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type', '')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                if self.json:
                    if self.status_code == 200:
                        if token == 'access_token':
                            self.data = AuthResponseSchema(**self.json)
                        else:
                            self.data = RefreshTokenResponseSchema(**self.json)
                        self.response_data = self.data.model_dump()

                        self.access_token = self.response_data.get(
                            'access_token'
                        )
                        if token == 'access_token':
                            self.refresh_token = self.response_data.get(
                                'refresh_token'
                            )
                        self.token_type = self.response_data.get('token_type')
                    else:
                        self.response_data = self.json
                        if self.status_code == 401:
                            if token == 'access_token':
                                self.expected_response_data = {
                                    'detail': 'Incorrect email or password'
                                }
                            else:
                                self.expected_response_data = {
                                    'detail': 'Could not validate '
                                    'refresh token'
                                }
            except requests.exceptions.JSONDecodeError:
                self.json = None
        else:
            self.json = None

    @allure.step('Assert tokens got')
    def assert_tokens(self):
        if self.response_data is None:
            pytest.fail('No response data available')

        assert self.access_token, 'Access token is missing'
        assert len(self.access_token) > 0, 'Access token is empty'

        assert self.refresh_token, 'Refresh token is missing'
        assert len(self.refresh_token) > 0, 'Refresh token is empty'

        assert self.token_type == 'bearer', 'Token type should be bearer'
