import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import YouGilePage


@pytest.mark.ui
@allure.title("Открытие задачи")
@allure.feature("Задачи")
@allure.story("Открытие задачи через UI")
def test_open_task() -> None:
    driver = webdriver.Chrome()

    task_name = "Diploma open task"

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

        with allure.step("Найти созданную задачу"):
            task = page.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@data-testid='board-task-title']"
                        f"//span[normalize-space()='{task_name}']"
                    )
                )
            )

        with allure.step("Открыть карточку задачи"):
            task.click()

        with allure.step("Проверить, что карточка открылась"):
            opened_task_title = page.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//span[normalize-space()='{task_name}']"
                    )
                )
            )

            assert opened_task_title.is_displayed(), (
                "Карточка задачи не открылась"
            )

    finally:
        driver.quit()