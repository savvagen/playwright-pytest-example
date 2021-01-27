from pages.web_elements import *
from pages.web_page import WebPage
import allure


class MainPage(WebPage):

    def account_button(self, username) -> WebElement: return el(self.page, selector='a[href="#@%s"]' % username)
    def loader(self) -> WebElement: return el(self.page, "text='Loading...'")
    def settings_link(self) -> WebElement: return el(self.page, selector='a[href="#settings"]')
    def editor_link(self) -> WebElement: return el(self.page, selector='a[href="#editor"]')
    def login_button(self)-> WebElement: return el(self.page, selector='a[href="#login"]')
    def register_button(self)-> WebElement: return el(self.page, element=s(self.page, 'text="Sign up"'))
    def articles(self)-> WebElementsCollection: return elc(self.page, elements=ss(self.page, ".article-preview"), element_container=Article)
    def nav_bar(self): return NavBar(self.page, "nav[class*='navbar']")

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    # Open Main Page
    @allure.step
    def open(self):
        self.page.goto("%s/#/" % self.base_url, wait_until="load")
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


class NavBar(WebElement):

    def __init__(self, page: Page, selector):
        super().__init__(page, selector=selector, element=None)

    def home_button(self): return el(self.page, element=self.element.query_selector("text='Home'"))
    def login_button(self): return el(self.page, element=self.element.query_selector("text='Sign in'"))
    def register_button(self): return el(self.page, element=self.element.query_selector("text='Sign up'"))


class Article(WebElement):

    def __init__(self, page: Page, element: ElementHandle):
        super().__init__(page, selector=None, element=element)

    def title(self): return el(self.page, element=self.element.query_selector("h1"))
    def body(self): return el(self.page, element=self.element.query_selector("p"))
