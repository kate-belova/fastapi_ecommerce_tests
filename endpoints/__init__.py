# fmt: off
__all__ = ['BaseAPI', 'HealthAPI', 'RootAPI', 'UsersAPI', 'AuthAPI']

from endpoints.base_api import BaseAPI
from endpoints.root.health_api import HealthAPI
from endpoints.root.root_api import RootAPI
from endpoints.users.users_api import UsersAPI
from endpoints.users.auth_api import AuthAPI
# fmt: on
