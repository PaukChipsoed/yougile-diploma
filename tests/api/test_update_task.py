import allure
import os

import pytest
import requests
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.api
@allure.title("Обновление задачи через API")
@allure.feature("Задачи")
@allure.story("Изменение задачи через API")
def test_update_task() -> None:
    base_url = "https://ru.yougile.com/api-v2"

    with allure.step("Получить данные авторизации"):
        token = os.getenv("YOUGILE_TOKEN")
        column_id = os.getenv("YOUGILE_COLUMN_ID")

        assert token, "Не найден YOUGILE_TOKEN в .env"
        assert column_id, "Не найден YOUGILE_COLUMN_ID в .env"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_body = {
        "title": "Задача для изменения",
        "columnId": column_id
    }

    with allure.step("Создать тестовую задачу"):
        create_response = requests.post(
            f"{base_url}/tasks",
            headers=headers,
            json=create_body
        )

    with allure.step("Проверить создание задачи"):
        assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    update_body = {
        "title": "Изменённая задача",
        "columnId": column_id
    }

    with allure.step("Обновить задачу"):
        update_response = requests.put(
            f"{base_url}/tasks/{task_id}",
            headers=headers,
            json=update_body
        )

    with allure.step("Проверить статус ответа 200"):
        assert update_response.status_code == 200
