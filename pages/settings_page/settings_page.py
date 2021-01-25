from pages.web_page import WebPage
from pages.main_page.main_page import MainPage
from pages.web_elements import *


class SettingsPage(WebPage):

    def logout_button(self): return el(self.page, selector='text="Or click here to logout."')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    # Open Settings Page
    def open(self):
        self.page.goto("%s/#/settings" % self.base_url, wait_until="load")
        return self

    def logout(self):
        self.logout_button().scroll_into_view().click()
        self.page.wait_for_selector('a[href="#login"]')
        return MainPage(self.base_url, self.page)
