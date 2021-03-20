from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from tests.e2e_tests.pom.page_manager import PageManager


class MainPage(PageManager):
    INPUT_URL = (By.NAME, 'url')
    INPUT_EMAIL = (By.NAME, 'email')

    BUTTON_SAVE_URL = (By.XPATH, '//input[@value="Save"]')
    BUTTON_SEND_EMAIL = (By.XPATH, '//input[@value="Send"]')

    BUTTON_UPDATE_URL = (By.XPATH, '//td[contains(text(), "{url}")]//parent::tr//button[contains(text(), "Update")]')
    BUTTON_DELETE_URL = (By.XPATH, '//td[contains(text(), "{url}")]//parent::tr//button[contains(text(), "Delete")]')

    BUTTON_CHANGE_URL = (By.XPATH, '//td[contains(text(), "{url}")]//input[@type="submit"]')
    INPUT_CHANGE_URL = (By.XPATH, '//td[contains(text(), "{url}")]//input[@type="url"]')

    TEXT_URL = (By.XPATH, '//div[@id="urls"]//td[contains(text(), "{url}")]')
    TEXT_ERROR_MESSAGE = (By.ID, 'error_message')

    def __init__(self, driver: webdriver.Chrome):
        super().__init__()
        self.driver = driver

    def send_email(self, email: str):
        self._type_email(email)
        self._click_send_email_button()
        return email

    def add_new_url(self, url: str):
        self._type_url(url)
        self._click_save_url_button()
        return url

    def update_url(self, url: str, new_url: str):
        self._click_update_url(url)
        self._type_change_url(url, new_url)
        self._click_change_url_button(url)
        alert_text = self.accept_alert_get_text()
        return {'new_url': new_url, 'alert_text': alert_text}

    def delete_url(self, url: str):
        self._click_delete_url_button(url)
        alert_text = self.accept_alert_get_text()
        self.wait_for_element_to_disappear(self.dynamic_locator(self.TEXT_URL, url=url))
        return alert_text

    def check_if_url_on_list(self, url: str, timeout: int = 20):
        url_on_list = self.dynamic_locator(self.TEXT_URL, url=url)
        try:
            self.wait_for_visibility_of_element(url_on_list, timeout)
        except NoSuchElementException:
            return False
        except TimeoutException:
            return False
        else:
            return True

    def get_error_message(self):
        return self.driver.find_element(*self.TEXT_ERROR_MESSAGE).text.strip()

    def _type_url(self, url: str):
        self.wait_and_type(self.INPUT_URL, url)
        return url

    def _click_save_url_button(self):
        self.wait_and_click(self.BUTTON_SAVE_URL)

    def _type_email(self, email: str):
        self.wait_and_type(self.INPUT_EMAIL, email)
        return email

    def _click_send_email_button(self):
        self.wait_and_click(self.BUTTON_SEND_EMAIL)

    def _click_update_url(self, url: str):
        button_update = self.dynamic_locator(self.BUTTON_UPDATE_URL, url=url)
        self.wait_and_click(button_update)

    def _click_delete_url_button(self, url: str):
        button_delete = self.dynamic_locator(self.BUTTON_DELETE_URL, url=url)
        self.wait_and_click(button_delete)

    def _type_change_url(self, url: str, new_url: str):
        input_change_url = self.dynamic_locator(self.INPUT_CHANGE_URL, url=url)
        self.wait_and_type(input_change_url, new_url)
        return new_url

    def _click_change_url_button(self, url: str):
        button_change_url = self.dynamic_locator(self.BUTTON_CHANGE_URL, url=url)
        self.wait_and_click(button_change_url)
