import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import YouGilePage


@pytest.mark.ui
@allure.title("Завершение задачи")
@allure.feature("Задачи")
@allure.story("Отметка задачи как выполненной через UI")
def test_complete_task() -> None:
    driver = webdriver.Chrome()

    task_name = "Diploma complete task"

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

        with allure.step("Открыть карточку задачи"):
            task = page.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@data-testid='board-task-title']"
                        f"//span[normalize-space()='{task_name}']"
                    )
                )
            )
            task.click()

        with allure.step("Отметить задачу как выполненную"):
            done_button = page.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='task-done-toggle']"
                    )
                )
            )
            done_button.click()

        with allure.step("Проверить, что задача выполнена"):
            completed_icon = page.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='task-done-toggle'] "
                        "[data-icon='IconCustomTaskDoneFilled']"
                    )
                )
            )

            assert completed_icon.is_displayed(), (
                "Задача не отмечена как выполненная"
            )

    finally:
        driver.quit()
