import pytest

from tests.e2e_tests.pom.main_page import MainPage


def test_add_url(get_driver, delete_url):
    driver = get_driver
    page = MainPage(driver)
    url = 'http://www.bbc.co.uk/music/genres/rockandindie/reviews.rss'
    page.add_new_url(url)
    assert page.check_if_url_on_list(url)


def test_delete_url(add_new_url):
    driver, url = add_new_url
    page = MainPage(driver)
    alert_text = page.delete_url(url)
    assert not page.check_if_url_on_list(url, 5)
    assert alert_text == 'URL Deleted.'


def test_update_url(add_new_url, delete_url):
    driver, url = add_new_url
    page = MainPage(driver)
    new_url = 'http://www.bbc.co.uk/music/genres/world/reviews.rss'
    r = page.update_url(url, new_url)
    assert page.check_if_url_on_list(new_url, 5)
    assert r['alert_text'] == 'URL modified'


@pytest.mark.xfail
def test_send_email(add_new_url, delete_url):
    driver, url = add_new_url
    page = MainPage(driver)
    page.send_email('example_mail@example.com')
    assert not page.get_error_message()
