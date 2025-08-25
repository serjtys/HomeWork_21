from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(f"=== АУТЕНТИФИКАЦИЯ ===")
        print(f"Email: {email}")
        print(f"Password: {password}")

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            print(f"Найден пользователь: {user}")
            print(f"Пароль совпадает: {user.check_password(password)}")

            if user.check_password(password):
                print("Успешная аутентификация!")
                return user
            else:
                print("Неверный пароль!")
                return None

        except UserModel.DoesNotExist:
            print("Пользователь не найден!")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None