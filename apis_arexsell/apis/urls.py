from ninja import NinjaAPI

from apis.modules.login.auth_router import router as auth_router
api = NinjaAPI()


api.add_router("/auth/", auth_router)
