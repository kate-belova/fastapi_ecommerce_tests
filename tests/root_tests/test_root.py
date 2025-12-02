import allure
import pytest


@pytest.mark.second
class TestRoot:
    @allure.feature('Deploy')
    @allure.story('Service greeting')
    @allure.title('Verify service is working')
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_service_greeting_success(self, root_api):
        root_api.get_service_greeting()
        root_api.assert_response_status(200)
        root_api.assert_greeting_message()
