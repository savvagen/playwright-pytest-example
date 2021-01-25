import pytest
from playwright.sync_api import Page
from pages.main_page.main_page import MainPage
from test.test_base import *
import logging
import re

logger = logging.getLogger("test")


@pytest.mark.only_browser("chromium")
def test_find_element_list(page: Page):
    main_page = MainPage(base_url, page)
    main_page.delete_cookies()
    main_page.open()

    main_page.loader().should_be_visible()
    main_page.loader().should_be_hidden()

    assert main_page.register_button().is_visible()
    pattern = re.compile(".*")

    assert main_page.articles().size() == 10
    assert main_page.articles().get(1).is_visible()
    assert pattern.match(main_page.articles().get(1).title().inner_text())
    assert pattern.match(main_page.articles().get(1).body().inner_text())
    logger.info(main_page.articles().get(2).title().inner_text())

    assert main_page.nav_bar().is_visible()
    assert main_page.nav_bar().login_button().is_visible()
    logger.info(main_page.nav_bar().login_button().inner_text())

    # articles = page.querySelectorAll(".article-preview")
    # assert len(articles) == 10
    # texts = page.evalOnSelectorAll(".article-preview h1", '''
    #     (elems, min) => {
    #         return elems.map(function(el) {
    #             return el.textContent    //.toUpperCase()
    #         });     //.join(", ");
    #     }''')
    # assert len(texts) == 10
    # assert not texts == []
    # assert articles[0].querySelector("h1").innerText() == "Python Playwright Demo"
    # assert articles[0].querySelector("p").innerText() == "Playwright Demo"
