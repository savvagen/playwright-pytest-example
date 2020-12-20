import allure
import pytest
from playwright.sync_api import Page, Browser
from models.user import User
from pages.registration_page.registration_page import RegistrationPage
from test.test_base import *


@pytest.yield_fixture(scope="function")
def reporting_fixture(browser: Browser, request):
    p: Page = browser.newPage()  # browser.newPage(videosPath="video/")
    p.context.clearCookies()
    yield p
    screenshot = p.screenshot(path=f"screenshots/{request.node.name}.png", fullPage=True)
    # video = p.video.path()
    p.close()
    allure.attach(screenshot, name=f"{request.node.name}", attachment_type=allure.attachment_type.PNG)
    # allure.attach.file(f'./{video}', attachment_type=allure.attachment_type.WEBM)


@allure.feature("Registration")
@allure.story("Valid Registration")
@allure.title("Register With new User")
@pytest.mark.only_browser("chromium")
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_should_register_new_user(reporting_fixture):
    page: Page = reporting_fixture
    register_page = RegistrationPage(base_url, page)
    user: User = User.fake_user()
    main_page = register_page.open().register_with(user)
    assert main_page.account_button(user.username).innerText() == user.username
    page.screenshot(path='screenshots/registered.png')



@allure.feature("Registration")
@allure.story("Invalid Registration")
@allure.title("Register With Existing Profile")
@pytest.mark.only_browser("chromium")
def test_should_not_register_with_same_creds(reporting_fixture):
    page: Page = reporting_fixture
    register_page = RegistrationPage(base_url, page)
    user: User = User(username=username, email=f"{username}@gmail.com", password="12345678")
    register_page = register_page.open()
    register_page.register_with(user)
    assert register_page.error_message().innerText() == "email has already been taken\nusername has already been taken"



@allure.feature("Registration")
@allure.story("Invalid Registration")
@allure.title("Register With Invalid Creds")
@pytest.mark.only_browser("chromium")
@pytest.mark.parametrize("user, error_text", [
    (
        User(username="", email=f"{fake.first_name()}{fake.last_name()}@gmail.com", password="12345678"),
        "username can't be blankis too short (minimum is 1 character)"
    ),
    (
        User(username="test.something", email=f"{fake.first_name()}{fake.last_name()}@gmail.com", password="123"),
        "password is too short (minimum is 8 characters)"
    ),
    (
        User(username="testsomething.testsomething", email=f"{fake.first_name()}{fake.last_name()}@gmail.com", password="123"),
        "username is too long (maximum is 20 characters)"
    )
])
def test_should_not_register_with_invalid_creds(reporting_fixture, user, error_text):
    page: Page = reporting_fixture
    register_page = RegistrationPage(base_url, page)
    register_page = register_page.open()
    register_page.register_with(user)
    assert error_text in register_page.error_message().innerText()