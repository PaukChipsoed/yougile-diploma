import allure
import os

import pytest
import requests
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.api
@allure.title("Получение задачи через API")
@allure.feature("Задачи")
@allure.story("Получение задачи через API")
def test_get_task() -> None:
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
        "title": "Задача для получения",
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

    with allure.step("Получить задачу по ID"):
        get_response = requests.get(
            f"{base_url}/tasks/{task_id}",
            headers=headers
        )

    with allure.step("Проверить статус ответа 200"):
        assert get_response.status_code == 200

    with allure.step("Проверить данные задачи"):
        task = get_response.json()

        assert task["id"] == task_id
        assert task["title"] == "Задача для получения"
        assert task["archived"] is False