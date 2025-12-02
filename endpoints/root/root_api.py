import allure
import requests

from endpoints import BaseAPI
from schemas import RootResponseSchema


class RootAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    @allure.step('Send GET request to check service greeting')
    def get_service_greeting(self):
        self.response = requests.get(self.base_url)
        self.status_code = self.response.status_code

        self.content_type = self.response.headers.get('content-type')
        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                self.data = RootResponseSchema(**self.json)
                self.response_data = self.data.model_dump()
            except requests.exceptions.JSONDecodeError:
                self.json = None
        else:
            self.json = None

    @allure.step('Assert service greeting')
    def assert_greeting_message(self):
        expected_data = {
            'message': 'Добро пожаловать в API интернет-магазина!'
        }
        self.assert_response_data(expected_data)
