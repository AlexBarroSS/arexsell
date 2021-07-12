
from django.db import models
from django.test import TestCase

from apis.modules.login.auth import UserLogin
from apis.models import User

default_user = {
    "name": "user",
    "password": "password",
    "email": "a@l.com",
}


class UserTestCase(TestCase):
    def test_login_class(self):
        login = UserLogin(
            name=default_user.get("name"),
            password=default_user.get("password"),
            email=default_user.get("email")
        )

        self.assertEquals(default_user.get("name"), login.name)
        self.assertEquals(default_user.get("password"), login.password)
        self.assertEquals(default_user.get("email"), login.email)

    def test_register_user_valid(self):
        setup_user = UserLogin(
            name=default_user.get("name"),
            password=default_user.get("password"),
            email=default_user.get("email")
        )

        setup_user.register_user()

        self.assertEquals(
            User.objects.get(
                name=setup_user.name
            ).name,
            setup_user.name
        )
