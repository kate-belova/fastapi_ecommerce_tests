import pytest
from sqlalchemy import select
from starlette import status
from starlette.exceptions import HTTPException

from database.connection import SessionLocal
from endpoints import UsersAPI
from endpoints.users.auth_api import AuthAPI
from models import UserModel
from tests.users_tests.test_data import valid_user_data


def delete_user(user_id: int):
    with SessionLocal() as db:
        get_user_stmt = select(UserModel).where(
            UserModel.id == user_id, UserModel.is_active == True
        )
        result = db.scalars(get_user_stmt)
        user = result.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found or inactive',
            )

        db.delete(user)
        db.commit()

        return {
            'status': 'success',
            'message': f'User with ID {user_id} successfully deleted',
        }


@pytest.fixture
def users_api(request):
    api = UsersAPI()
    created_user_ids = []

    original_register = api.register_new_user

    def add_user_with_tracking(user_data, validate=True):
        result = original_register(user_data, validate=validate)
        if api.id and api.id not in created_user_ids:
            created_user_ids.append(api.id)
        return result

    api.register_new_user = add_user_with_tracking

    def cleanup():
        if created_user_ids:
            for user_id in created_user_ids:
                delete_user(user_id)

    request.addfinalizer(cleanup)
    return api


@pytest.fixture
def registered_user(users_api):
    users_api.register_new_user(valid_user_data[0])

    users_api.assert_response_status(201)
    users_api.assert_response_data(valid_user_data[0])
    users_api.assert_new_user_in_db()

    return {
        'username': users_api.email,
        'password': valid_user_data[0]['password'],
    }


@pytest.fixture
def authenticated_user(registered_user, auth_api):
    auth_data = registered_user
    auth_api.get_token('access_token', auth_data)

    auth_api.assert_response_status(200)
    auth_api.assert_tokens()

    return auth_api


@pytest.fixture
def auth_api():
    return AuthAPI()
