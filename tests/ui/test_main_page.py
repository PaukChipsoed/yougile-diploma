import allure
import pytest
from selenium import webdriver

from pages import YouGilePage


@pytest.mark.ui
@allure.title("Открытие главной страницы")
@allure.feature("Главная страница")
@allure.story("Открытие YouGile")
def test_open_you_gile() -> None:
    driver = webdriver.Chrome()

    try:
        page = YouGilePage(driver)

        with allure.step("Открыть YouGile"):
            page.open()

        with allure.step("Проверить заголовок страницы"):
            assert "управления проектами и задачами" in page.get_title()

    finally:
        driver.quit()