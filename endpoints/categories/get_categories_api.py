import allure
import requests

from endpoints import BaseAPI
from schemas import CategoryResponseSchema


class GetCategoriesAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/categories/'
        self.categories = None

    @allure.step('Send GET request to get all categories')
    def get_categories(self):
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type', '')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()
                if self.json:
                    self.categories = [
                        CategoryResponseSchema(**category_data)
                        for category_data in self.json
                    ]
            except requests.exceptions.JSONDecodeError:
                self.json = None
        else:
            self.json = None

    @allure.step('Assert categories count is {count}')
    def assert_categories_count(self, count: int):
        actual_count = len(self.categories)
        assert (
            actual_count == count
        ), f'Expected {count} categories, but got {actual_count}'

    @allure.step('Assert hierarchy is valid')
    def assert_hierarchy_ids_are_valid(self):
        all_ids = {category.id for category in self.categories}

        for category in self.categories:
            if category.parent_id is not None:
                assert category.parent_id in all_ids, (
                    f'Category {category.id} references non-existent '
                    f'parent_id {category.parent_id}'
                )
                assert (
                    category.parent_id != category.id
                ), f'Category {category.id} references itself as parent'

    @allure.step('Assert all categories are active')
    def assert_all_categories_active(self):
        inactive_categories = [
            category for category in self.categories if not category.is_active
        ]
        assert len(inactive_categories) == 0, (
            f'Found {len(inactive_categories)} inactive categories: '
            f'{[category.id for category in inactive_categories]}'
        )
