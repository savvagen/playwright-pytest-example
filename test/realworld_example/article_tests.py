from playwright.sync_api import Page
import pytest, requests, time, allure
from pages.realworld_example.editor_page.editor_page import EditorPage
from pages.realworld_example.article_page.article_page import ArticlePage
from pages.realworld_example.login_page.login_page import LoginPage
from pages.realworld_example.main_page.main_page import MainPage
from pages.realworld_example.settings_page.settings_page import SettingsPage


base_url = "https://react-redux.realworld.io"
username = "savva.genchevskiy"
password = "S.gench19021992"

article = {
    'title': 'Python Playwright Demo',
    'subject': 'Playwright Demo',
    'body': "\n# Hello World\n\nSome `text` \n\nSome function:\n```\ndef function():\n     pass\n```\n"
}


def login_with_api(email, password):
    headers = {"content-type": "application/json; charset=utf-8"}
    json = {"user": {"email": email, "password": password}}
    return requests.post("https://conduit.productionready.io/api/users/login", json=json, headers=headers)


@pytest.yield_fixture(scope="function") # scope="module" - to run all tests in one browser context
def log_in_fixture(browser, request):
    p: Page = browser.newPage()  # browser.newPage(videosPath="video/")
    # A) SetUp from Cookies
    resp = login_with_api(username+"@gmail.com", password)
    cookie = {"name": "__cfduid", "value": resp.cookies.get('__cfduid'), "domain": ".productionready.io", "path": "/",
              "httpOnly": True, "sameSite": "Lax"}
    playwright_cookies = [cookie]
    # 3. Open Web Page
    main_page = MainPage(base_url, p).open()
    # 4. Set Cookies and put JWT token to Local Storage
    p.evaluate("(t) => { localStorage.setItem('jwt', `${t}`) }", arg=resp.json()['user']['token'])
    p.context.addCookies(playwright_cookies)
    # 5. Enjoy!!! Reload Page as Logged In User
    main_page.page.reload(waitUntil="load")
    # B) SetUp from UI
    # LoginPage(base_url, p).open().login(username+"@gmail.com", password)\
    #     .account_button(username).shouldBeVisible()
    yield p
    # Logout
    # SettingsPage(base_url, p).open().logout()
    screenshot = p.screenshot(path=f"screenshots/{request.node.name}.png", fullPage=True)
    # video = p.video.path()
    p.close()
    allure.attach(screenshot, name=f"{request.node.name}", attachment_type=allure.attachment_type.PNG)
    # allure.attach.file(f'./{video}', attachment_type=allure.attachment_type.WEBM)


@allure.feature("Article")
@allure.story("Publish Article")
@allure.title("Publish Article Flow from MainPage")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.only_browser("chromium")
def test_should_publish_article_from_main(log_in_fixture):
    p: Page = log_in_fixture
    editor_page = MainPage(base_url, p).open_editor()
    article_page = editor_page.publish_article(article['title'], article['subject'], article['body'])
    assert article_page.title().innerText() == article['title']


@allure.feature("Article")
@allure.story("Publish Article")
@allure.title("Publish Article Flow from ArticlePage")
@pytest.mark.only_browser("chromium")
def test_should_publish_article(log_in_fixture):
    p: Page = log_in_fixture
    editor_page = EditorPage(base_url, p).open()
    article_page = editor_page.publish_article(article['title'], article['subject'], article['body'])
    assert article_page.title().shouldBeVisible().innerText() == article['title']



# def test_should_create_post(log_in_fixture):
#     p: Page = log_in_fixture
#     title = "Python Playwright Demo"
#     body = "\n# Hello World\n\nSome `text` \n\nSome function:\n```\ndef function():\n     pass\n```\n"
#     p.click('a[href="#editor"]')
#     p.fill('input[placeholder="Article Title"]', title)
#     p.fill('input[placeholder="What\'s this article about?"]', 'Playwright Demo')
#     p.fill('textarea[placeholder="Write your article (in markdown)"]', body)
#     p.click('text="Publish Article"')
#     assert p.innerText("h1") == title
#     p.screenshot(path='new_post.png')
