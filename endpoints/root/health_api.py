import allure
import requests

from endpoints import BaseAPI
from schemas import HealthResponseSchema


class HealthAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/health'

    @allure.step('Send GET request to check service health')
    def check_health(self):
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code

        self.content_type = self.response.headers.get('content-type')
        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                self.data = HealthResponseSchema(**self.json)
                self.response_data = self.data.model_dump()
            except requests.exceptions.JSONDecodeError:
                self.json = None
                self.actual_error_message = 'Invalid JSON response'
        else:
            self.json = None
            self.actual_error_message = self.response.text

    @allure.step('Assert health data is the one expected')
    def assert_health_data(self):
        expected_data = {'status': 'healthy', 'service': 'FastAPI Ecommerce'}
        self.assert_data(expected_data)
        self.assert_valid_timestamp()
