from elements.playwright_element import *
from pages.web_page import WebPage
from pages.main_page.main_page import MainPage
from models.user import User
import allure


class LoginPage(WebPage):

    # Define wrapped Playwright Elements
    def email_filed(self): return el(self.page, 'input[type="email"]')
    def password_field(self): return el(self.page, 'input[type="password"]')
    def submit_button(self): return el(self.page, 'button[type="submit"]')
    def error_message(self): return el(self.page, '.error-messages > li')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url
        self.s = lambda css: self.page.querySelector(css)

    # Open Login Page
    @allure.step
    def open(self):
        self.page.goto("%s/#/login" % self.base_url, waitUntil="load")
        return self

    # Authorize
    @allure.step('Login user with email: "{email}", password: "{password}"')
    def login(self, email, password):
        self.email_filed().val(email).pressTab()
        self.password_field().val(password).pressEnter()
        # self.password_field().val(password)
        # self.submit_button().click()
        return MainPage(self.base_url, self.page)

    @allure.step('Login with user: "{1}"')
    def login_with(self, user: User):
        self.email_filed().val(user.email).pressTab()
        self.password_field().val(user.password)
        self.submit_button().click()
        return MainPage(self.base_url, self.page)

    # def login(self, email, password):
    #     elf.s(css='input[type="email"]').fill(email)
    #     self.s(css='input[type="password"]').fill(password)
    #     self.s(css='button[type="submit"]').click()
