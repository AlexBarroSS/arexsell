
import random
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
    def test_user_class(self):
        setup_user = UserLogin(
            name=user_json.get("name"),
            password=user_json.get("password"),
            email=user_json.get("email")
        )

        self.assertEquals(
            setup_user.is_correct_password(user_json.get("password")), True)

    def test_register_user_valid(self):
        is_registred = user_object.register_user()

        self.assertEquals(is_registred.get('success'), True)

        user_registred = UserLogin.get_user_by_name(user_object.name)

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

        is_user_altered = user_object_altered.update_user()

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
            user_object.is_correct_password(ramdom_password), True)
