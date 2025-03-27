import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.careers_page import CareersPage

@pytest.fixture

def driver():
    driver = webdriver.Chrome()  # Make sure ChromeDriver is installed and in PATH
    driver.maximize_window()
    yield driver
    driver.quit()


def test_careers_page_is_opened(driver):
    careers_page = CareersPage(driver)
    careers_page.open("https://useinsider.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("Insider"))
    assert "Insider" in driver.title, "Insider homepage is not opened."

    # Navigate to Careers Page
    careers_page.open_careers_page()

    # Check if Careers page is opened
    assert careers_page.is_careers_page_opened(), "Careers page is not opened."

    # Check if required sections are present
    careers_page.are_sections_present()  # No assertion, just printing results