
import requests
import random

from requests.auth import HTTPBasicAuth
from django.test import TestCase

from apis.modules.login.auth import UserLogin

user_json = {
    "name": "user",
    "password": "password",
    "email": "alex@gmail.com",
}

user_json_altered = {
    "name": "user",
    "password": "password",
    "email": "afonso@gmail.com",
}

user_object = UserLogin(
    name=user_json.get("name"),
    password=user_json.get("password"),
    email=user_json.get("email")
)

user_object_altered = UserLogin(
    name=user_json_altered.get("name"),
    password=user_json_altered.get("password"),
    email=user_json_altered.get("email")
)

user_object_with_email_invalid = UserLogin(
    name=user_json.get("name"),
    password=user_json.get("password"),
    email="email@invalid"
)


class UserTestCase(TestCase):
    def test_register_user_valid(self):
        is_registred = user_object.register_user()

        self.assertEquals(is_registred.get('success'), True)

        user_registred = UserLogin.get_user(user_object.name)

        self.assertEquals(user_registred.get('success'), True)
        self.assertEquals(user_registred.get(
            'user').get('name'), user_object.name)

    def test_register_user_invalid(self):
        is_registred = user_object_with_email_invalid.register_user()

        self.assertEquals(is_registred.get('success'), False)
        self.assertEquals(is_registred.get('user'), None)

    def test_update_user(self):
        is_registred = user_object.register_user()

        self.assertEquals(is_registred.get('success'), True)

        user_id = UserLogin.get_user_by_id(
            is_registred.get("user").get("id")).get("user").get("id")

        self.assertEquals(user_id, is_registred.get("user").get("id"))

        is_user_altered = user_object_altered.update_user(user_id)

        self.assertEquals(is_user_altered.get("success"), True)
        self.assertEquals(is_user_altered.get('user')
                          .get('name'), user_object_altered.name)
        self.assertEquals(is_user_altered.get('user')
                          .get('email'), user_object_altered.email)

    def test_password(self):
        random_number = random.randint(10000000000, 90000000000)
        ramdom_password = str(random_number)

        user_object.password = UserLogin.encrypt_password(ramdom_password)

        self.assertNotEquals(ramdom_password, user_object.password)
        self.assertEquals(
            user_object.is_correct_password(ramdom_password, user_object.password), True)

    def test_get_user(self):
        is_registred = user_object.register_user()

        self.assertEquals(is_registred.get('success'), True)

        user_registred = UserLogin.get_user(user_object.name)

        self.assertTrue(UserLogin.is_correct_password(
            user_object.password, user_registred.get('user').get('password')))

        self.assertEquals(user_registred.get(
            'user').get('name'), user_object.name)
        self.assertEquals(user_registred.get(
            'user').get('email'), user_object.email)

        user_id = user_registred.get("user").get("id")

        user_by_id = UserLogin.get_user_by_id(user_id).get("user")

        self.assertEquals(user_id, user_by_id.get("id"))

    def test_login(self):
        is_registred = user_object.register_user()

        self.assertEquals(is_registred.get('success'), True)

        user = UserLogin.get_user(user_object.name)

        self.assertEquals(user.get('success'), True)

        self.assertTrue(UserLogin.is_correct_password(
            user_object.password, user.get('user').get('password')))


key = {"kid": "ID", "thumbprint": "DFPAiAxsWHAu3vSpg4Q4Nl-z_q5c2kVtdo8pwG18uBg"}

base_url = 'http://127.0.0.1:8000'


class LoginTestCase(TestCase):
    def test_login_get_token_unauthorized(self):
        response = requests.get(f'{base_url}/api/auth',
                                auth=HTTPBasicAuth("admin", "secret")).json()
        self.assertEquals(response.get("token").get("success"), False)

    def test_login_get_token_ok(self):
        response = requests.get(
            f'{base_url}/api/auth',
            auth=HTTPBasicAuth(user_object.name, user_object.password)).json()

        self.assertEquals(response.get("token").get("success"), True)

        response = requests.get(
            f'{base_url}/api/auth',
            auth=HTTPBasicAuth(user_object.name, user_object.password)).json()

        self.assertEquals(response.get("token").get("success"), True)
