from ninja import NinjaAPI

from ninja.security import django_auth
from ninja.security import HttpBearer
from ninja.security import HttpBasicAuth

api = NinjaAPI()


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        if username == "admin" and password == "secret":
            return username


@api.get("/auth", auth=BasicAuth())
def bearer(request):
    return {"token": request.auth}
