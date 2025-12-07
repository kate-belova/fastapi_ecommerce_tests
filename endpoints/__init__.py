# fmt: off
__all__ = ['BaseAPI', 'HealthAPI', 'RootAPI', 'UsersAPI', 'AuthAPI',
           'GetCategoriesAPI', 'PostCategoryAPI', 'PutCategoryAPI',
           'DeleteCategoryAPI']

from endpoints.base_api import BaseAPI
from endpoints.root.health_api import HealthAPI
from endpoints.root.root_api import RootAPI
from endpoints.users.users_api import UsersAPI
from endpoints.users.auth_api import AuthAPI
from endpoints.categories.get_categories_api import GetCategoriesAPI
from endpoints.categories.post_category_api import PostCategoryAPI
from endpoints.categories.put_category_api import PutCategoryAPI
from endpoints.categories.delete_category_api import DeleteCategoryAPI
# fmt: on
