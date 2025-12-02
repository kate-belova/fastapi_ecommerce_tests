import allure
import requests
from sqlalchemy import select

from database.connection import SessionLocal
from endpoints import BaseAPI
from models import UserModel
from schemas import UserResponseSchema, UserCreateRequestSchema


class UsersAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/users/'
        self.id = None
        self.email = None

    @allure.step('Send POST request to register new user')
    def register_new_user(self, user_data=None, validate=True):
        payload = user_data
        if user_data:
            if validate:
                payload = UserCreateRequestSchema(**user_data).model_dump()

        self.response = requests.post(self.url, json=payload)
        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type')

        if 'application/json' in self.content_type:
            try:
                self.json = self.response.json()

                if self.status_code in (200, 201) and self.json:
                    self.data = UserResponseSchema(**self.json)
                    self.response_data = self.data.model_dump()
                    self.id = self.response_data.get('id')
                    self.email = self.response_data.get('email')
                else:
                    self.response_data = self.json

            except requests.exceptions.JSONDecodeError:
                self.json = None
        else:
            self.json = None

    @allure.step('Assert new user is in database')
    def assert_new_user_in_db(self):
        with SessionLocal() as db:
            get_user_stmt = select(UserModel).where(
                UserModel.id == self.id,
                UserModel.email == self.email,
                UserModel.is_active == True,
            )
            result = db.scalars(get_user_stmt)
            user = result.first()
            assert user, f'New user is not found in database'
