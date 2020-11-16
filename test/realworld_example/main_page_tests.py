import pytest
from playwright.sync_api import Page
from pages.realworld_example.main_page.main_page import MainPage
from test.realworld_example.test_base import *


@pytest.mark.only_browser("chromium")
def test_find_element_list(page: Page):
    main_page = MainPage(base_url, page)
    main_page.deleteCookies()
    main_page.open()
    page.waitForSelector("div[class='container page'] .article-preview h1", state="visible")
    articles = page.querySelectorAll(".article-preview")
    assert len(articles) == 10
    texts = page.evalOnSelectorAll(".article-preview h1", '''
        (elems, min) => {
            return elems.map(function(el) {
                return el.textContent    //.toUpperCase()
            });     //.join(", ");
        }''')
    assert len(texts) == 10
    assert not texts == []
    assert articles[0].querySelector("h1").innerText() == "Python Playwright Demo"
    assert articles[0].querySelector("p").innerText() == "Playwright Demo"
