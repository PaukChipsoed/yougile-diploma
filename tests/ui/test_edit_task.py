import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4

from pages import YouGilePage


@pytest.mark.ui
@allure.title("Редактирование задачи")
@allure.feature("Задачи")
@allure.story("Изменение названия задачи через UI")
def test_edit_task() -> None:
    driver = webdriver.Chrome()

    unique_id = uuid4().hex[:8]
    task_name = f"Diploma edit task {unique_id}"
    edited_task_name = f"Diploma edited task {unique_id}"

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
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@data-testid='board-task-title']"
                        f"//span[normalize-space()='{task_name}']"
                    )
                )
            )

        with allure.step("Открыть карточку задачи"):
            task.click()

        with allure.step("Найти кнопку редактирования"):
            title = page.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='board-task-title']"
                    )
                )
            )

            ActionChains(driver).move_to_element(title).perform()

            edit_button = page.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "[data-testid='board-task-pancel']"
                    )
                )
            )

        with allure.step("Изменить название задачи"):
            edit_button.click()

            active_element = driver.switch_to.active_element
            active_element.send_keys(Keys.CONTROL, "a")
            active_element.send_keys(edited_task_name)
            active_element.send_keys(Keys.ENTER)

        with allure.step("Проверить новое название"):
            edited_task = page.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//span[normalize-space()='{edited_task_name}']"
                    )
                )
            )

            assert edited_task.is_displayed(), (
                "Название задачи не изменилось"
            )

    finally:
        driver.quit()
