from pages.web_page import WebPage
from pages.realworld_example.main_page.main_page import MainPage
from elements.playwright_element import *


class SettingsPage(WebPage):

    def logout_button(self): return el(self.page, 'text="Or click here to logout."')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    # Open Settings Page
    def open(self):
        self.page.goto("%s/#/settings" % self.base_url, waitUntil="load")
        return self

    def logout(self):
        self.logout_button().scrollIntoView().click()
        self.page.waitForSelector('a[href="#login"]')
        return MainPage(self.base_url, self.page)
