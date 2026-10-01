import allure
import os

import pytest
import requests
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.api
@allure.title("Создание задачи с пустым названием")
@allure.feature("Задачи")
@allure.story("Валидация создания задачи через API")
def test_create_task_empty_title() -> None:
    base_url = "https://ru.yougile.com/api-v2"

    with allure.step("Получить данные авторизации"):
        token = os.getenv("YOUGILE_TOKEN")
        column_id = os.getenv("YOUGILE_COLUMN_ID")

        assert token, "Не найден YOUGILE_TOKEN в .env"
        assert column_id, "Не найден YOUGILE_COLUMN_ID в .env"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
        "title": "",
        "columnId": column_id
    }

    with allure.step("Отправить запрос с пустым названием"):
        response = requests.post(
            f"{base_url}/tasks",
            headers=headers,
            json=body
        )

    with allure.step("Проверить статус ответа 400"):
        assert response.status_code == 400

    with allure.step("Проверить тело ответа"):
        response_body = response.json()

        assert response_body["statusCode"] == 400
        assert "title should not be empty" in response_body["message"]
        assert response_body["error"] == "Bad Request"
