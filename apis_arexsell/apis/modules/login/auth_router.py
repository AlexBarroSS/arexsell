import jwt
import datetime

from ninja import Router
from ninja.security import HttpBasicAuth

from apis.modules.login.auth import UserLogin

router = Router()

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


@ router.get("/", auth=BasicAuth())
def basic(request):
    return {"token": request.auth}


@ router.post("/register")
def register(request, username: str, password: str, email: str):
    user = UserLogin(name=username, password=password, email=email)

    is_user_registred = user.register_user()

    return is_user_registred


@ router.get("/user/{user_id}", auth=BasicAuth())
def get_user_by_id(request, user_id: int):
    return UserLogin.get_user_by_id(user_id)


@ router.put("/user/{user_id}", auth=BasicAuth())
def update_user(request, user_id: int, username: str, password: str, email: str):
    user_data = UserLogin.get_user_by_id(user_id)

    if not user_data.get("success"):
        return user_data

    user_update = UserLogin(name=username,
                            password=password, email=email)

    return user_update.update_user(user_id)
