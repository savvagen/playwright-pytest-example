from elements.playwright_element import *
from pages.web_page import WebPage
from pages.realworld_example.main_page.articles import *
import allure


class MainPage(WebPage):

    def account_button(self, username): return el(self.page, 'a[href="#@%s"]' % username)
    def settings_link(self): return el(self.page, 'a[href="#settings"]')
    def editor_link(self): return el(self.page, 'a[href="#editor"]')
    def login_button(self): return el(self.page, 'a[href="#login"]')
    def register_button(self): return el(self.page, 'text="Sign up"')
    def articles(self): return Articles(self.page, ".article-preview")

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    # Open Main Page
    @allure.step
    def open(self):
        self.page.goto("%s/#/" % self.base_url, waitUntil="load")
        return self

    @allure.step("Press SignIn button")
    def login(self):
        self.login_button().click()
        from pages.realworld_example.login_page.login_page import LoginPage
        return LoginPage(self.base_url, self.page)

    @allure.step("Press Register button")
    def register(self):
        self.register_button().click()
        from pages.realworld_example.registration_page.registration_page import RegistrationPage
        return RegistrationPage(self.base_url, self.page)

    @allure.step("Press Settings link")
    def open_settings(self):
        self.settings_link().click()
        from pages.realworld_example.settings_page.settings_page import SettingsPage
        return SettingsPage(self.base_url, self.page)

    @allure.step("Press Editor link")
    def open_editor(self):
        self.editor_link().click()
        from pages.realworld_example.editor_page.editor_page import EditorPage
        return EditorPage(self.base_url, self.page)
