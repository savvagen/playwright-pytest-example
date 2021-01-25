import pytest, allure
from playwright.sync_api import Page, Browser
from pages.login_page.login_page import LoginPage
from test.test_base import *


# yield_fixture(scope="session") #### To run all test in one browser (Fixture is running ones per session)
# yield_fixture(scope="function") #### To run all test in separated browsers (Fixture Is Running for every test)
@pytest.fixture(scope="function")
def logout_fixture(browser: Browser, request):
    # p: Page = browser.new_page()
    p: Page = browser.new_page(record_video_dir="video/")
    p.context.clear_cookies()
    yield p
    # Logout
    # main_page = MainPage(base_url, p)
    # if p.inner_text(main_page.account_button(username).selector) is not None or "":
    #     settings_page = main_page.open_settings()
    #     settings_page.logout()
    screenshot = p.screenshot(path=f"screenshots/{request.node.name}.png", full_page=True)
    video = p.video.path()
    p.close()
    allure.attach(screenshot, name=f"{request.node.name}", attachment_type=allure.attachment_type.PNG)
    allure.attach.file(f'./{video}', attachment_type=allure.attachment_type.WEBM)


@allure.feature("Login")
@allure.story("Login Flow")
@allure.title("Login With Valid Credentials")
@allure.description_html("""
<h1>Main Login Scenario</h1>
<h3>Test Description</h3>
""")
@pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.only_browser("chromium")
def test_should_login_to_system(logout_fixture):
    page: Page = logout_fixture
    login_page = LoginPage(base_url, page)
    main_page = login_page.open().login("%s@gmail.com" % username, password)
    assert main_page.account_button(username).inner_text() == username
    assert "%s/#/" % base_url in page.url


@allure.feature("Login")
@allure.story("Login Flow")
@allure.title("Login With Invalid Credentials")
@pytest.mark.only_browser("chromium")
def test_should_not_login_with_invalid_credentials(logout_fixture):
    page: Page = logout_fixture
    login_page = LoginPage(base_url, page)
    login_page.open().login("%s@gmail.comm" % username, password)
    assert login_page.error_message().inner_text() == "email or password is invalid"
    assert login_page.email_filed().value() == "%s@gmail.comm" % username
    assert login_page.submit_button().is_enabled()
    assert "%s/#/login" % base_url in page.url


@allure.feature("Login")
@allure.story("Logout")
@allure.title("Logout from System")
@pytest.mark.only_browser("chromium")
def test_should_logout_from_system(logout_fixture):
    page: Page = logout_fixture
    login_page = LoginPage(base_url, page)
    main_page = login_page.open() \
        .login("%s@gmail.com" % username, password) \
        .open_settings() \
        .logout()
    assert main_page.login_button().inner_text() == "Sign in"
    assert main_page.register_button().inner_text() == "Sign up"


@pytest.mark.only_browser("chromium")
def test_should_login(page: Page):
    page.context.clear_cookies()
    page.goto('%s/#/login' % base_url)
    page.fill('input[type="email"]', "%s@gmail.com" % username)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"]')  # page.click('text="Sign in"')
    # Use `s(css)` function
    # s: ElementHandle = lambda css: page.querySelector(css)
    # page.context.clearCookies()
    # page.goto('%s/#/login' % base_url)
    # s('input[type="email"]').fill("%s@gmail.com" % username)
    # s('input[type="password"]').fill("S.gench19021992")
    # s('button[type="submit"]').click()
    assert page.wait_for_selector('a[href="#@%s"]' % username).inner_text() == username
    assert page.inner_text('a[href="#@%s"]' % username) == username
    assert "%s/#/" % base_url in page.url
    page.screenshot(path='screenshots/logged_in.png')
