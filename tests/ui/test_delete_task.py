import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages import YouGilePage


@pytest.mark.ui
def test_delete_task() -> None:
    driver = webdriver.Chrome()

    try:
        page = YouGilePage(driver)

        page.open()
        page.login()
        page.select_project()
        page.click_add_task()
        page.create_task("Task for deletion")

        task = page.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@data-testid='board-task-title']"
                    "//span[normalize-space()='Task for deletion']"
                )
            )
        )
        task.click()

        menu_button = page.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "[data-testid='board-task-menu']"
                )
            )
        )
        menu_button.click()

        delete_menu_item = page.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Удалить']"
                )
            )
        )
        delete_menu_item.click()

        confirm_delete_button = page.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[normalize-space()='Удалить']"
                )
            )
        )
        confirm_delete_button.click()

        page.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@data-testid='board-task-title']"
                    "//span[normalize-space()='Task for deletion']"
                )
            )
        )

    finally:
        driver.quit()
