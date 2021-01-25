import pytest, requests, allure
import logging
from playwright.sync_api import Page
from pages.editor_page.editor_page import EditorPage
from pages.main_page.main_page import MainPage
from models.article import Article, fake_article
from test.test_base import *

logger = logging.getLogger(__name__)


def login_with_api(email, password):
    headers = {"content-type": "application/json; charset=utf-8"}
    json = {"user": {"email": email, "password": password}}
    return requests.post("https://conduit.productionready.io/api/users/login", json=json, headers=headers)


@pytest.fixture(scope="function")  # scope="module" - to run all tests in one browser context
def log_in_fixture(browser, request):
    p: Page = browser.new_page()  # browser.new_page(record_video_dir="video/")
    # A) SetUp from Cookies
    resp = login_with_api(username+"@gmail.com", password)
    cookie = {"name": "__cfduid",
              "value": resp.cookies.get('__cfduid'),
              "domain": ".productionready.io",
              "path": "/", "httpOnly": True, "sameSite": "Lax"}
    # 3. Open Web Page
    main_page = MainPage(base_url, p).open()
    # 4. Set Cookies and put JWT token to Local Storage
    p.evaluate("(t) => { localStorage.setItem('jwt', `${t}`) }", arg=resp.json()['user']['token'])
    p.context.add_cookies([cookie])
    # 5. Enjoy!!! Reload Page as Logged In User
    main_page.page.reload(wait_until="load")
    main_page.account_button(username).should_be_visible()
    # B) SetUp from UI
    # LoginPage(base_url, p).open().login(username+"@gmail.com", password)\
    #     .account_button(username).shouldBeVisible()
    yield p
    # Logout
    # SettingsPage(base_url, p).open().logout()
    screenshot = p.screenshot(path=f"screenshots/{request.node.name}.png", full_page=True)
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
    article = fake_article()
    editor_page = MainPage(base_url, p).open_editor()
    article_page = editor_page.publish_article(article)
    assert article_page.title().inner_text() == article.title


@allure.feature("Article")
@allure.story("Publish Article")
@allure.title("Publish Article Flow from ArticlePage")
@pytest.mark.only_browser("chromium")
def test_should_publish_article(log_in_fixture):
    p: Page = log_in_fixture
    article: Article = fake_article()
    editor_page = EditorPage(base_url, p).open()
    article_page = editor_page.publish_article(article)
    assert article_page.title().should_be_visible().inner_text() == article.title


def test_should_create_post(log_in_fixture):
    p: Page = log_in_fixture
    title = "Python Playwright Demo"
    body = "\n# Hello World\n\nSome `text` \n\nSome function:\n```\ndef function():\n     pass\n```\n"
    p.click('a[href="#editor"]')
    p.fill('input[placeholder="Article Title"]', title)
    p.fill('input[placeholder="What\'s this article about?"]', 'Playwright Demo')
    p.fill('textarea[placeholder="Write your article (in markdown)"]', body)
    p.click('text="Publish Article"')
    assert p.inner_text("h1") == title
    p.screenshot(path='screenshots/new_post.png')
