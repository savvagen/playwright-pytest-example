import pytest, allure, time, os, pathlib
from playwright.sync_api import Page, Request, Browser, BrowserContext, Video
from pages.realworld_example.login_page.login_page import LoginPage
from pages.realworld_example.main_page.main_page import MainPage
from pages.realworld_example.settings_page.settings_page import SettingsPage
from faker import Faker

fake = Faker(['en_US'])
base_url = "https://react-redux.realworld.io"
username = 'savva.genchevskiy'
password = "S.gench19021992"


# yield_fixture(scope="session") #### To run all test in one browser (Fixture is running ones per session)
# yield_fixture(scope="function") #### To run all test in separated browsers (Fixture Is Running for every test)
@pytest.yield_fixture(scope="function")
def logout_fixture(browser: Browser, request):
    p: Page = browser.newPage()  # browser.newPage(videosPath="video/")
    p.context.clearCookies()
    yield p
    # Logout
    # main_page = MainPage(base_url, p)
    # if p.innerText(main_page.account_button(username).selector) is not None or "":
    #     settings_page = main_page.open_settings()
    #     settings_page.logout()
    screenshot = p.screenshot(path=f"screenshots/{request.node.name}.png", fullPage=True)
    # video = p.video.path()
    p.close()
    allure.attach(screenshot, name=f"{request.node.name}", attachment_type=allure.attachment_type.PNG)
    # allure.attach.file(f'./{video}', attachment_type=allure.attachment_type.WEBM)


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
    assert main_page.account_button(username).innerText() == username
    assert "%s/#/" % base_url in page.url
    # page.screenshot(path='screenshots/logged_in.png')


@allure.feature("Login")
@allure.story("Login Flow")
@allure.title("Login With Invalid Credentials")
@pytest.mark.only_browser("chromium")
def test_should_not_login_with_invalid_credentials(logout_fixture):
    page: Page = logout_fixture
    login_page = LoginPage(base_url, page)
    login_page.open().login("%s@gmail.comm" % username, password)
    assert login_page.error_message().innerText() == "email or password is invalid"
    assert login_page.email_filed().value() == "%s@gmail.comm" % username
    assert login_page.submit_button().isEnabled()
    assert "%s/#/login" % base_url in page.url
    # page.screenshot(path='screenshots/invalid_login.png')


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
    assert main_page.login_button().innerText() == "Sign in"
    assert main_page.register_button().innerText() == "Sign up"
    # page.screenshot(path='screenshots/logged_out.png')




# @pytest.mark.only_browser("chromium")
# def test_should_login(page: Page):
#     page.context.clearCookies()
#     page.goto('%s/#/login' % base_url)
#     page.fill('input[type="email"]', "savva.genchevskiy@gmail.com")
#     page.fill('input[type="password"]', "S.gench19021992")
#     page.click('button[type="submit"]')  # page.click('text="Sign in"')
#     # Use `s(css)` function
#     # s: ElementHandle = lambda css: page.querySelector(css)
#     # page.context.clearCookies()
#     # page.goto('%s/#/login' % base_url)
#     # s('input[type="email"]').fill("%s@gmail.com" % username)
#     # s('input[type="password"]').fill("S.gench19021992")
#     # s('button[type="submit"]').click()
#     assert page.waitForSelector('a[href="#@%s"]' % username).innerText() == username
#     assert page.innerText('a[href="#@%s"]' % username) == username
#     assert "%s/#/" % base_url in page.url
#     page.screenshot(path='logged_in.png')
#
#
# @pytest.mark.only_browser("chromium")
# def test_find_element_list(page: Page):
#     main_page = MainPage(base_url, page)
#     main_page.deleteCookies()
#     main_page.open()
#     page.waitForSelector("div[class='container page'] .article-preview h1", state="visible")
#     articles = page.querySelectorAll(".article-preview")
#     assert len(articles) == 10
#     texts = page.evalOnSelectorAll(".article-preview h1", '''
#         (elems, min) => {
#             return elems.map(function(el) {
#                 return el.textContent    //.toUpperCase()
#             });     //.join(", ");
#         }''')
#     print(texts)
#     assert len(texts) == 10
#     assert not texts == []
#     #assert articles[0].querySelector("h1").innerText() == "test"
#     #assert articles[0].querySelector("p").innerText() == "test"
