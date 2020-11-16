from playwright.sync_api import Page, ElementHandle
from elements.playwright_element import xel


class Articles:

    def __init__(self, page: Page, selector):
        self.page = page
        self.selector = selector
        self.element_list = self.page.querySelectorAll(self.selector)

    def size(self):
        return len(self.element_list)

    def get(self, index):
        return Article(self.page, self.element_list[index])


class Article:

    def __init__(self, page: Page, element_handle: ElementHandle):
        self.page = page
        self.el = element_handle

    def link(self): return xel(page=self.page, css=None, el=self.el.querySelector(".preview-link"))
    def title(self): return xel(page=self.page, css=None, el=self.el.querySelector("h1"))
    def body(self): return xel(page=self.page, css=None, el=self.el.querySelector("p"))
