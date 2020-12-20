from elements.playwright_element import *
from pages.web_page import WebPage
import allure


class MainPage(WebPage):

    def account_button(self, username): return el(self.page, 'a[href="#@%s"]' % username)
    def settings_link(self): return el(self.page, 'a[href="#settings"]')
    def editor_link(self): return el(self.page, 'a[href="#editor"]')
    def login_button(self): return el(self.page, 'a[href="#login"]')
    def register_button(self): return el(self.page, 'text="Sign up"')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url
        self.articles_list = Articles(self.page)

    # Open Main Page
    @allure.step
    def open(self):
        self.page.goto("%s/#/" % self.base_url, waitUntil="load")
        return self

    @allure.step("Press SignIn button")
    def login(self):
        self.login_button().click()
        from pages.login_page.login_page import LoginPage
        return LoginPage(self.base_url, self.page)

    @allure.step("Press Register button")
    def register(self):
        self.register_button().click()
        from pages.registration_page.registration_page import RegistrationPage
        return RegistrationPage(self.base_url, self.page)

    @allure.step("Press Settings link")
    def open_settings(self):
        self.settings_link().click()
        from pages.settings_page.settings_page import SettingsPage
        return SettingsPage(self.base_url, self.page)

    @allure.step("Press Editor link")
    def open_editor(self):
        self.editor_link().click()
        from pages.editor_page.editor_page import EditorPage
        return EditorPage(self.base_url, self.page)



class Articles:

    def __init__(self, page: Page):
        self.page = page

    def articles(self): return els(self.page, css=".article-preview")

    def get(self, index): return Article(self.page, self.articles().get(index))


class Article:

    def __init__(self, page: Page, element_handle: ElementHandle):
        self.page = page
        self.element_handle = element_handle

    def title(self): return elh(self.page, el=self.element_handle.querySelector("h1"))
    def body(self): return elh(self.page, el=self.element_handle.querySelector("p"))