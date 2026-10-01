import allure
import os

import pytest
import requests
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.api
@allure.title("Создание задачи через API")
@allure.feature("Задачи")
@allure.story("Создание задачи через API")
def test_create_task() -> None:
    url = "https://ru.yougile.com/api-v2/tasks"

    with allure.step("Получить данные авторизации"):
        token = os.getenv("YOUGILE_TOKEN")
        column_id = os.getenv("YOUGILE_COLUMN_ID")

        assert token, "Не найден YOUGILE_TOKEN в .env"
        assert column_id, "Не найден YOUGILE_COLUMN_ID в .env"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    body = {
        "title": "test task",
        "columnId": column_id
    }

    with allure.step("Отправить запрос на создание задачи"):
        response = requests.post(
            url,
            headers=headers,
            json=body
        )

    with allure.step("Проверить статус ответа 201"):
        assert response.status_code == 201
