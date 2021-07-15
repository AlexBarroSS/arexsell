import json
import jwt
import datetime

from ninja import NinjaAPI
from ninja.security import django_auth
from ninja.security import HttpBearer
from ninja.security import HttpBasicAuth

from apis.modules.login.auth import UserLogin

api = NinjaAPI()

KEY = "DFPAiAxsWHAu3vSpg4Q4Nl-z_q5c2kVtdo8pwG18uBg"


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = UserLogin.get_user(username)

        if (user.get('success')):
            if (UserLogin.is_correct_password(password, user.get('user').get('password'))):

                return {
                    "success": True,
                    "data": jwt.encode(
                        {
                            "user": user.get("user"),
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
                        },
                        KEY,
                        algorithm="HS256",
                    )
                }
            return {"success": False}
        return {"success": False}


@ api.get("/auth", auth=BasicAuth())
def basic(request):
    return {"token": request.auth}


@ api.post("/register")
def register(request, username: str, password: str, email: str):
    user = UserLogin(name=username, password=password, email=email)

    is_user_registred = user.register_user()

    return is_user_registred


@ api.get("/user/{user_id}", auth=BasicAuth())
def get_user_by_id(request, user_id: int):
    return UserLogin.get_user_by_id(user_id)


@ api.put("/user/{user_id}", auth=BasicAuth())
def update_user(request, user_id: int, username: str, password: str, email: str):
    user_data = UserLogin.get_user_by_id(user_id)

    if not user_data.get("success"):
        return user_data

    user_update = UserLogin(name=username,
                            password=password, email=email)

    return user_update.update_user(user_id)
