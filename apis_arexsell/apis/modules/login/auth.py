import bcrypt
from django.core.validators import validate_email

from apis.models import User


class UserLogin:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def register_user(self):
        try:
            user = User.objects.create(
                name=self.name,
                password=UserLogin.encrypt_password(self.password),
                email=self.email
            )

            validate_email(user.email)
            user.save()

            return {'success': True, 'user': UserLogin.user_to_json(user, without_password=True)}

        except:
            return {'success': False, 'user': None}

    def update_user(self, id):
        try:
            validate_email(self.email)

            user = User.objects.get(id=id)

            user.name = self.name
            user.email = self.email
            if user.password != self.password:
                user.password = UserLogin.encrypt_password(self.password)
            user.save()

            return {'success': True, 'user': UserLogin.user_to_json(user, without_password=True)}
        except:
            return {'success': False, 'user': None}

    @staticmethod
    def get_user(name):
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

    @staticmethod
    def get_user_by_id(id):
        try:
            user = User.objects.get(id=id)
            return {
                'success': True,
                'user': UserLogin.user_to_json(user)
            }
        except:
            return {
                'success': False,
                'user': None
            }

    @staticmethod
    def is_correct_password(password, hash):
        try:
            if bcrypt.checkpw(str.encode(password), str.encode(hash)):
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
    def user_to_json(user, without_password=False):
        user_json = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password
        }

        if without_password:
            user_json.pop("password")

        return user_json
