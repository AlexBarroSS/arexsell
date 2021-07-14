from apis.modules.login.auth import UserLogin
from ninja import NinjaAPI

from ninja.security import django_auth
from ninja.security import HttpBearer
from ninja.security import HttpBasicAuth

api = NinjaAPI()


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = UserLogin.get_user(username)

        if (user.get('success')):
            if (UserLogin.is_correct_password(password, user.get('user').get('password'))):
                return True
            return False
        return False


@api.post("/register")
def register(request, username: str, password: str, email: str):
    user = UserLogin(name=username, password=password, email=email)

    is_user_registred = user.register_user()

    return is_user_registred


@api.get("/user/{user_id}", auth=BasicAuth())
def get_user_by_id(request, user_id: int):
    return UserLogin.get_user_by_id(user_id)


@api.put("/user/{user_id}", auth=BasicAuth())
def update_user(request, user_id: int, username: str, password: str, email: str):
    user_data = UserLogin.get_user_by_id(user_id)

    if not user_data.get("success"):
        return user_data

    user_update = UserLogin(name=username,
                            password=password, email=email)

    return user_update.update_user(user_id)
