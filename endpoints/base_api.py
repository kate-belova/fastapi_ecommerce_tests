from datetime import datetime, timezone

import allure
import requests


class BaseAPI:
    def __init__(self):
        self.base_url = 'https://fastapi-ecommerce.online/'
        self.response = requests.Response
        self.status_code = None
        self.content_type = None
        self.json = None
        self.data = None
        self.response_data = None

    @allure.step('Assert response status is {status}')
    def assert_response_status(self, status):
        assert (
            self.status_code == status
        ), f'Expected status code {status}, but got {self.status_code}'

    def assert_response_data(self, expected_data, ignore_missing_fields=True):
        for key, value in expected_data.items():
            if ignore_missing_fields and key not in self.response_data:
                continue

            assert (
                key in self.response_data
            ), f'Field {key} is missing in response'
            assert self.response_data[key] == value, (
                f'Expected {key} to be {value}, '
                f'but got {self.response_data[key]}'
            )

    @allure.step('Assert timestamp is valid and recent')
    def assert_valid_timestamp(
        self, timestamp_field: str = 'timestamp', max_diff_seconds: int = 30
    ):
        timestamp = self.response_data.get(timestamp_field)
        assert (
            timestamp is not None
        ), f'Timestamp field "{timestamp_field}" is missing'

        try:
            timestamp_str = str(timestamp)
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1] + '+00:00'

            response_time = datetime.fromisoformat(timestamp_str)

            if response_time.tzinfo is None:
                response_time = response_time.replace(tzinfo=timezone.utc)

            current_time = datetime.now(timezone.utc)
            time_diff = (current_time - response_time).total_seconds()

            assert (
                time_diff >= -5
            ), f'Timestamp is too far in the future: {time_diff} seconds'

            assert (
                time_diff <= max_diff_seconds
            ), f'Timestamp is too old. Difference: {time_diff:.2f} seconds'

        except (ValueError, AttributeError) as invalid_format_error:
            raise AssertionError(
                f'Invalid timestamp format: {timestamp}. '
                f'Error: {invalid_format_error}'
            )
