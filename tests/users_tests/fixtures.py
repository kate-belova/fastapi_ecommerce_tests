import pytest
from sqlalchemy import select
from starlette import status
from starlette.exceptions import HTTPException

from database.connection import SessionLocal
from endpoints import UsersAPI, AuthAPI
from models import UserModel
from tests.users_tests.users_test_data import valid_user_data


def delete_user_by_email(user_email: str):
    with SessionLocal() as db:
        get_user_stmt = select(UserModel).where(
            UserModel.email == user_email, UserModel.is_active == True
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
            'message': f'User with email {user_email} successfully deleted',
        }


@pytest.fixture
def users_api(request):
    api = UsersAPI()
    created_user_emails = []

    original_register = api.register_new_user

    def add_user_with_tracking(user_data, validate=True):
        user_email = user_data.get('email')
        result = original_register(user_data, validate=validate)

        cleanup_email = api.email or user_email
        if cleanup_email and cleanup_email not in created_user_emails:
            created_user_emails.append(cleanup_email)

        return result

    api.register_new_user = add_user_with_tracking

    def cleanup():
        for user_email in created_user_emails:
            try:
                delete_user_by_email(user_email)
            except Exception as e:
                print(f'Note: Could not delete user {user_email}: {e}')

    request.addfinalizer(cleanup)
    return api


@pytest.fixture
def registered_buyer(users_api):
    user_data = valid_user_data[0]
    users_api.register_new_user(user_data)

    if users_api.status_code != 409:
        users_api.assert_response_status(201)
        users_api.assert_response_data(user_data)

    users_api.assert_new_user_in_db()

    return {
        'username': users_api.email,
        'password': user_data['password'],
    }


@pytest.fixture
def registered_seller(users_api):
    user_data = valid_user_data[1]
    users_api.register_new_user(user_data)

    if users_api.status_code != 409:
        users_api.assert_response_status(201)
        users_api.assert_response_data(user_data)

    users_api.assert_new_user_in_db()

    return {
        'username': users_api.email,
        'password': user_data['password'],
    }


@pytest.fixture
def authenticated_buyer(registered_buyer, auth_api):
    auth_data = registered_buyer
    auth_api.get_token('access_token', auth_data)

    auth_api.assert_response_status(200)
    auth_api.assert_tokens()

    return auth_api


@pytest.fixture
def authenticated_seller(registered_seller, auth_api):
    auth_data = registered_seller
    auth_api.get_token('access_token', auth_data)

    auth_api.assert_response_status(200)
    auth_api.assert_tokens()

    return auth_api


@pytest.fixture
def auth_api():
    return AuthAPI()
