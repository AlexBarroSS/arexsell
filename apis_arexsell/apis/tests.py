import jwt
import requests
import random
import datetime
import time

from requests.auth import HTTPBasicAuth
from django.test import TestCase

from apis.modules.login.auth import UserLogin


KEY = "DFPAiAxsWHAu3vSpg4Q4Nl-z_q5c2kVtdo8pwG18uBg"
base_url = 'http://127.0.0.1:8000'


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


class LoginTestCase(TestCase):
    def test_login_get_token_unauthorized(self):
        response = requests.get(f'{base_url}/api/auth/',
                                auth=HTTPBasicAuth("admin", "secret")).json()
        self.assertEquals(response.get("token").get("success"), False)

    def test_login_get_token_ok(self):
        response = requests.get(
            f'{base_url}/api/auth/',
            auth=HTTPBasicAuth(user_object.name, user_object.password)).json()

        data_jwt = jwt.decode(
            str.encode(response.get("token").get("data")),
            KEY,
            algorithms=["HS256"]
        )

        self.assertEquals(response.get("token").get("success"), True)
        self.assertEquals(response.get("token").get("success"), True)

        self.assertNotEquals(response.get("token").get("data"), data_jwt)

        self.assertEquals(data_jwt.get("user").get("name"), user_object.name)


class JWTTestCase(TestCase):
    def test_jwt_encrypt_expired(self):
        jwt_payload = jwt.encode(
            {"exp": datetime.datetime.utcnow() + datetime.timedelta(microseconds=10)
             },
            KEY,
            algorithm="HS256",
        )

        time.sleep(1)

        jwt_payload_expired = False
        try:
            jwt.decode(
                jwt_payload,
                KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            jwt_payload_expired = True

        self.assertEqual(jwt_payload_expired, True)

    def test_jwt_encrypt_not_expired(self):
        jwt_payload = jwt.encode(
            {"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1)
             },
            KEY,
            algorithm="HS256",
        )

        jwt_payload_expired = False
        try:
            jwt.decode(
                jwt_payload,
                KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            jwt_payload_expired = True

        self.assertEqual(jwt_payload_expired, False)

    def test_jwt_data(self):
        jwt_payload = jwt.encode(
            {
                "data": "OK",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1)
            },
            KEY,
            algorithm="HS256",
        )

        try:
            jwt_decode = jwt.decode(
                jwt_payload,
                KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            jwt_decode = "expired"

        self.assertNotEquals(jwt_decode, "expired")
        self.assertNotEquals(jwt_decode, jwt_payload)

        self.assertEquals(jwt_decode.get("data"), 'OK')
