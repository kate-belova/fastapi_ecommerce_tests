import allure
import requests

from endpoints import BaseAPI
from schemas import CategoryCreateRequestSchema


class PutCategoryAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/categories/'
        self.headers = {}

    @allure.step('Send PUT request to fully update category')
    def put_category(self, category_data, category_id=None, token=None):
        if category_id:
            self.url += f'{category_id}'

        payload = CategoryCreateRequestSchema(**category_data).model_dump()

        if token:
            self.headers['Authorization'] = f'Bearer {token}'

        self.response = requests.put(
            self.url, json=payload, headers=self.headers
        )
        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type', '')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                if self.json:
                    self.response_data = self.json

                    if self.status_code == 401:
                        self.expected_response_data = {
                            'detail': 'Not authenticated'
                        }
                    elif self.status_code == 403:
                        self.expected_response_data = {
                            'detail': 'Обновлять категории могут '
                            'только администраторы'
                        }
            except requests.exceptions.JSONDecodeError:
                self.json = None
        else:
            self.json = None
