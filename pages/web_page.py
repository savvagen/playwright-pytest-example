from playwright.sync_api import Page
from playwright.sync_api import ElementHandle
from elements.playwright_element import *


class WebPage(object):
    def __init__(self, page: Page):
        self.page = page

    def deleteCookies(self):
        self.page.context.clearCookies()

    def reload(self):
        self.page.reload(waitUntil="load")
