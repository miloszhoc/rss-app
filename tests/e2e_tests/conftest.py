from selenium import webdriver
import pytest
import requests
import configparser
from tests.e2e_tests.driver import CreateDriver

config = configparser.ConfigParser()
config.read('tests/e2e_tests/test_config.ini')


@pytest.fixture()
def get_driver():
    driver = CreateDriver()
    # driver.set_driver('chrome', 'local', 'tests/e2e_tests/drivers/chromedriver.exe', '--headless')
    driver.set_driver('chrome', 'remote', '--headless')
    driver = driver.get_current_driver()
    driver.get(config['TEST_ENV']['APP_URL'])

    yield driver

    driver.quit()


@pytest.fixture()
def add_new_url(get_driver):
    driver: webdriver.Chrome = get_driver
    url = 'https://www.polsatsport.pl/rss/tenis.xml'
    r = requests.post(config['TEST_ENV']['APP_URL'] + '/urls', data={'url': url})
    driver.refresh()
    assert r.json()['success'] == True
    return driver, url


@pytest.fixture()
def delete_url():
    yield
    url = requests.get(config['TEST_ENV']['APP_URL'] + '/urls')
    r = requests.delete(config['TEST_ENV']['APP_URL'] + '/urls/' + str(url.json()[0]['id']))
    assert r.json()['success'] == True
