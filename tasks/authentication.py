import base64

from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class EnvironmentBasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Получаем данные из заголовков
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        if not auth_header.startswith("Basic "):
            return None

        try:
            auth_decoded = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
            username, password = auth_decoded.split(":")
        except (TypeError, ValueError):
            raise AuthenticationFailed("Invalid basic header")

        expected_username = settings.BASIC_AUTH_USERNAME
        expected_password = settings.BASIC_AUTH_PASSWORD

        if username == expected_username and password == expected_password:
            return (User(username=username), None)

        raise AuthenticationFailed("Invalid credentials")
