import os
from typing import Dict, Any

import requests

from imageTaskAPI.settings import env


class FaceCloudAPI:
    """
    Класс для взаимодействия с API FaceCloud для обработки изображений и получения данных о лицах.
    """

    def __init__(self, demographics: bool = True):
        self.base_url = env("FACE_CLOUD_API_URL")
        self.headers = {"Content-Type": "application/json"}
        self.demographics = demographics
        self.api_key = None

    def get_url(self, endpoint: str, params: Dict[str, Any] = None) -> str:
        """
        Формирует URL с параметрами запроса для API FaceCloud.

        :param endpoint: Конечная точка API.
        :param params: Параметры запроса (по умолчанию None).
        :return: URL для запроса к API FaceCloud.
        """
        url = f"{self.base_url}/{endpoint}"
        if params:
            url += f"?{'&'.join(f'{key}={value}' for key, value in params.items())}"
        return url

    def send_request(
        self,
        endpoint: str,
        data: Any = None,
        params: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        url = self.get_url(endpoint, params)
        try:
            response = requests.post(url, headers=self.headers, data=data, json=json)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print()
            raise Exception(
                f"Произошла ошибка при запросе к внешнему api: {str(e)} {response.json()}"
            )

    def process_image(self, image_path: str):
        """
        Отправляет изображение на API FaceCloud для обработки и возвращает данные о лицах.

        :param image_path: Путь к изображению.
        :return: Данные о лицах или пустой список в случае ошибки.
        """
        if not self.api_key:
            self.api_key = self.__get_api_key()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "image/jpeg",
        }
        with open(image_path, "rb") as img_file:
            response = self.send_request(
                "api/v1/detect",
                data=img_file,
                params={"demographics": self.demographics},
            )
        return response.get("data", [])

    def __get_api_key(self) -> str:
        email = os.getenv("FACE_CLOUD_EMAIL") or env("FACE_CLOUD_EMAIL")
        password = os.getenv("FACE_CLOUD_PASSWORD") or env("FACE_CLOUD_PASSWORD")
        api_key = self.send_request(
            "api/v1/login", json={"email": email, "password": password}
        )
        return api_key.get("data").get("access_token")


facecloud = FaceCloudAPI()
