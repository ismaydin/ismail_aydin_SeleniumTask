from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class CareersPage(BasePage):
    COMPANY_MENU = (By.LINK_TEXT, "Company")  # More reliable locator
    CAREERS_LINK = (By.LINK_TEXT, "Careers")
    LOCATIONS_SECTION = (By.XPATH, "//*[@id='career-our-location']/div/div/div/div[1]/h3")
    TEAMS_SECTION = (By.XPATH, "//*[@id='career-find-our-calling']/div/div/a")
    LIFE_AT_INSIDER_SECTION = (By.XPATH, "/html/body/div[1]/section[4]/div/div/div/div[1]/div/h2")
    QUALITY_ASSURANCE_BUTTON = (By.LINK_TEXT, "Quality Assurance")
    SEE_ALL_QA_JOBS_BUTTON = (By.LINK_TEXT, "See all QA jobs")
    LOCATION_FILTER_RENDERED = (By.ID, "select2-filter-by-location-container")
    LOCATION_FILTER_CLEAR_BUTTON = (By.CLASS_NAME, "select2-selection__clear")

    def open_careers_page(self):
        company_menu = self.find_element(self.COMPANY_MENU)
        ActionChains(self.driver).move_to_element(company_menu).click().perform()
        self.click(self.CAREERS_LINK)

    def is_careers_page_opened(self):
        return "careers" in self.driver.current_url

    def are_sections_present(self):
        sections = {
            "Locations Section": self.LOCATIONS_SECTION,
            "Teams Section": self.TEAMS_SECTION,
            "Life at Insider Section": self.LIFE_AT_INSIDER_SECTION
        }

        all_present = True
        for name, locator in sections.items():
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
                print(f"{name} is found on the page.")
            except:
                print(f"{name} is NOT found on the page.")
                all_present = False

        self.click_element(self.TEAMS_SECTION, "Teams")
        self.click_element(self.QUALITY_ASSURANCE_BUTTON, "Quality Assurance")
        self.click_element(self.SEE_ALL_QA_JOBS_BUTTON, "See all QA jobs")

        self.filter_jobs()
        return all_present

    def click_element(self, locator, element_name):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"Clicked on the '{element_name}' button.")
            time.sleep(2)
        except:
            try:
                element = self.find_element(locator)
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Clicked on the '{element_name}' button via JavaScript.")
                time.sleep(2)
            except:
                print(f"Failed to click on the '{element_name}' button.")

    def filter_jobs(self):
        print("Applying filters...")

        # Step 1: Click the 'x' clear button if it exists
        try:
            clear_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.LOCATION_FILTER_CLEAR_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", clear_button)
            print("Cleared location filter.")
            time.sleep(1)
        except:
            print("No clear button for location filter found.")

        # Step 2: Defocus
        try:
            self.driver.execute_script("document.body.click();")
            print("Clicked empty space to defocus.")
            time.sleep(1)
        except Exception as e:
            print(f"Error clicking empty space: {e}")

        # Step 3: Select location using Select2 dropdown logic
        try:
            location_dropdown_xpath = "//span[contains(@class, 'select2-selection') and contains(@aria-labelledby, 'select2-filter-by-location-container')]"
            location_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, location_dropdown_xpath))
            )

            self.driver.execute_script("arguments[0].style.border='3px solid blue'", location_dropdown)
            print("Highlighted location dropdown box.")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_dropdown)
            time.sleep(1)
            location_dropdown.click()
            print("Clicked location dropdown box.")
            time.sleep(1)
            location_dropdown.click()
            print("Clicked location dropdown box.")
            time.sleep(1)

            time.sleep(1)
            location_items = self.driver.find_elements(By.XPATH, "//li[contains(@id, 'select2-filter-by-location-result')]")
            if not location_items or (len(location_items) == 1 and location_items[0].text.strip() == "All"):
                print("Dropdown seems to only show 'All'. Trying to refocus and re-fetch.")
                location_dropdown.click()
                time.sleep(1)
                location_items = self.driver.find_elements(By.XPATH, "//li[contains(@id, 'select2-filter-by-location-result')]")

            for item in location_items:
                print(f"Hovering over location option: {item.text.strip()}")
                ActionChains(self.driver).move_to_element(item).perform()
                time.sleep(0.2)
                if item.text.strip().startswith("Istanbul"):
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                    ActionChains(self.driver).move_to_element(item).perform()
                    time.sleep(0.3)
                    ActionChains(self.driver).move_to_element(item).click().perform()
                    print("Selected Location: " + item.text.strip())
                    time.sleep(2)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".position-list-item"))
                    )
                    break
        except Exception as e:
            print(f"Failed to select location: {e}")

        # Step 4: Select department by clicking the full dropdown control
        try:
            dropdown_xpath = "//span[contains(@class, 'select2-selection') and contains(@aria-labelledby, 'select2-filter-by-department-container')]"
            dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

            self.driver.execute_script("arguments[0].style.border='3px solid red'", dropdown)
            print("Highlighted department dropdown box.")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            time.sleep(1)
            dropdown.click()
            print("Clicked department dropdown box.")
            time.sleep(1)

            department_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@id, 'select2-filter-by-department-result')]"))
            )

            for item in department_items:
                ActionChains(self.driver).move_to_element(item).perform()
                time.sleep(0.2)
                if item.text.strip().startswith("Quality"):
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                    ActionChains(self.driver).move_to_element(item).perform()
                    time.sleep(0.3)
                    try:
                        ActionChains(self.driver).move_to_element(item).click().perform()
                    except Exception as stale:
                        print("Stale element detected. Refetching department list and retrying...")
                        item = self.driver.find_element(By.XPATH, f"//li[contains(@id, 'select2-filter-by-department-result') and contains(text(), 'Quality Assurance')]")
                        ActionChains(self.driver).move_to_element(item).click().perform()
                    print("Selected Department: " + item.text.strip())
                    time.sleep(6)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".position-list-item"))
                    )
                    break
        except Exception as e:
            print(f"Failed to select department: {e}")

        time.sleep(5)
        # Step 5: Count job results
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "deneme"))
            )
            result_count_elem = self.driver.find_element(By.ID, "deneme")
            result_count = result_count_elem.text.strip()
            print(f"Number of filtered job listings (from span): {result_count}")
            print("Pausing for visual confirmation of filtered results...")
            time.sleep(5)

            jobs = self.driver.find_elements(By.CSS_SELECTOR, ".position-list-item")
            # Step 6: Select the specific QA job by title text
            target_title = "Software QA Tester / Intercontinental Support - Insider Testinium Tech Hub (Fresh Graduate - Remote)"
            for job in jobs:
                try:
                    title_elem = job.find_element(By.CSS_SELECTOR, "p.position-title")
                    if title_elem.text.strip() == target_title:
                        print("Target job found. Clicking on it...")
                        view_button = job.find_element(By.CSS_SELECTOR, "a.btn.btn-navy")
                        self.driver.execute_script("arguments[0].click();", view_button)
                        WebDriverWait(self.driver, 10).until(EC.url_changes(self.driver.current_url))
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        print("Navigated to job details page.")
                        time.sleep(3)
                        time.sleep(5)
                        break
                except Exception as e:
                    print(f"Error checking job: {e}")
        except Exception as e:
            print(f"Failed to count job listings: {e}")
