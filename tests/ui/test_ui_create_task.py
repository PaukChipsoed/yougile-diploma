import allure
import pytest
from selenium import webdriver

from pages import YouGilePage


@pytest.mark.ui
@allure.title("Создание задачи")
@allure.feature("Задачи")
@allure.story("Создание задачи через UI")
def test_create_task() -> None:
    driver = webdriver.Chrome()

    task_name = "Diploma unique task"

    try:
        page = YouGilePage(driver)

        with allure.step("Открыть YouGile"):
            page.open()

        with allure.step("Авторизоваться"):
            page.login()

        with allure.step("Открыть проект 1234"):
            page.select_project()

        with allure.step("Нажать «Добавить задачу»"):
            page.click_add_task()

        with allure.step(f"Создать задачу «{task_name}»"):
            page.create_task(task_name)

        with allure.step("Проверить, что задача появилась на доске"):
            assert page.task_is_visible(
                task_name
            ), "Задача не появилась на доске"

    finally:
        driver.quit()