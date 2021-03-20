from selenium.common.exceptions import NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


class PageManager():

    def __init__(self):
        super().__init__()
        self.driver: webdriver.Chrome = None

    def wait_and_click(self, locator: tuple, timeout: int = 20) -> None:
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
        WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(locator))
        self.driver.find_element(*locator).click()

    def wait_for_visibility_of_element(self, locator: tuple, timeout: int = 20) -> None:
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    def wait_and_type(self, locator: tuple, text: str, timeout: int = 20) -> None:
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def dynamic_locator(self, locator: tuple, *args, **kwargs) -> tuple:
        return (locator[0], locator[1].format(*args, **kwargs))

    def accept_alert_get_text(self, timeout: int = 20):
        try:
            WebDriverWait(self.driver, timeout).until(ec.alert_is_present())
        except NoAlertPresentException:
            pass
        else:
            alert, text = self.driver.switch_to.alert, self.driver.switch_to.alert.text.strip()
            alert.accept()
            return text

    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = 20):
        WebDriverWait(self.driver, timeout).until(ec.invisibility_of_element(locator))
