import allure
import pytest


@pytest.mark.first
class TestHealth:
    @allure.feature('Deploy')
    @allure.story('Health')
    @allure.title('Verify service health')
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_health_check_success(self, health_api):
        health_api.check_health()
        health_api.assert_response_is_200()
        health_api.assert_health_data()
