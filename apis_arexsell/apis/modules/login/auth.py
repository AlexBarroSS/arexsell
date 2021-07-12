from apis.models import User


class UserLogin:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def register_user(self):
        model_user = User.objects.create(
            name=self.name,
            password=self.password,
            email=self.email
        )

        model_user.save()

        return model_user.name
