import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()


class YouGilePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self) -> None:
        self.driver.get("https://ru.yougile.com")

    def get_title(self) -> str:
        return self.driver.title

    def login(self) -> None:
        email = os.getenv("YOUGILE_EMAIL")
        password = os.getenv("YOUGILE_PASSWORD")

        assert email, "Не найден YOUGILE_EMAIL в .env"
        assert password, "Не найден YOUGILE_PASSWORD в .env"

        login_link = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[@href='/team/' and contains(., 'Войти')]"
                )
            )
        )
        login_link.click()

        email_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[autocomplete='email']"
                )
            )
        )
        email_input.clear()
        email_input.send_keys(email)

        password_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[autocomplete='current-password']"
                )
            )
        )
        password_input.clear()
        password_input.send_keys(password)

        sign_in_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@role='button' and .//div[normalize-space()='Войти']]"
                )
            )
        )
        sign_in_button.click()

        self.wait.until(
            lambda driver: (
                driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'truncate') and "
                    "normalize-space()='1234']"
                )
                or driver.find_elements(
                    By.XPATH,
                    "//span[normalize-space()='Добавить задачу']"
                )
            )
        )

    def select_project(self) -> None:
        project = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'truncate') and "
                    "normalize-space()='1234']"
                )
            )
        )
        project.click()

    def click_add_task(self) -> None:
        add_task_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[normalize-space()='Добавить задачу']"
                )
            )
        )
        add_task_button.click()

    def create_task(self, task_name: str) -> None:
        task_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '[data-testid="board-task-input-name"]'
                )
            )
        )

        task_input.send_keys(task_name)
        task_input.send_keys("\n")

    def task_is_visible(self, task_name: str) -> bool:
        task = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@data-testid='board-task-title']"
                    f"//span[normalize-space()='{task_name}']"
                )
            )
        )

        return task.is_displayed()