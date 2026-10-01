import allure
import os

import pytest
import requests
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.api
@allure.title("Получение несуществующей задачи")
@allure.feature("Задачи")
@allure.story("Обработка ошибки 404")
def test_get_nonexistent_task() -> None:
    base_url = "https://ru.yougile.com/api-v2"

    with allure.step("Получить данные авторизации"):
        token = os.getenv("YOUGILE_TOKEN")

        assert token, "Не найден YOUGILE_TOKEN в .env"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    task_id = "00000000-0000-0000-0000-000000000000"

    with allure.step("Запросить несуществующую задачу"):
        response = requests.get(
            f"{base_url}/tasks/{task_id}",
            headers=headers
        )

    with allure.step("Проверить статус ответа 404"):
        assert response.status_code == 404

    with allure.step("Проверить тело ответа"):
        body = response.json()

        assert body["statusCode"] == 404
        assert body["message"] == "Задача не найдена"