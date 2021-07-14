import bcrypt
from django.core.validators import validate_email

from apis.models import User


class UserLogin:
    def __init__(self, name, password, email):
        self.name = name
        self.password = UserLogin.encrypt_password(password)
        self.email = email

    def register_user(self):
        user = User.objects.create(
            name=self.name,
            password=self.password,
            email=self.email
        )

        try:
            validate_email(user.email)
            user.save()

            return {'success': True, 'user': UserLogin.user_to_json(user)}

        except:
            return {'success': False, 'user': None}

    def update_user(self):
        try:
            validate_email(self.email)

            user = User.objects.get(name=self.name)

            user.email = self.email
            user.password = self.password
            user.save()

            return {'success': True, 'user': UserLogin.user_to_json(user)}
        except:
            return {'success': False, 'user': None}

    @staticmethod
    def get_user_by_name(name):
        try:
            user = User.objects.get(name=name)
            return {
                'success': True,
                'user': UserLogin.user_to_json(user)
            }
        except:
            return {
                'success': False,
                'user': None
            }

    def is_correct_password(self, password):
        try:
            if bcrypt.checkpw(str.encode(password), str.encode(self.password)):
                return True
            return False
        except:
            return False

    @staticmethod
    def encrypt_password(password):
        try:
            hashed_password = bcrypt.hashpw(
                str.encode(password), bcrypt.gensalt())
            return hashed_password.decode("utf-8")
        except:
            return False

    @ staticmethod
    def user_to_json(user):
        return {
            "name": user.name,
            "email": user.email
        }
