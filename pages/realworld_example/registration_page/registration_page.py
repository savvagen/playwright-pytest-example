from elements.playwright_element import *
from pages.web_page import WebPage
from pages.realworld_example.main_page.main_page import MainPage
from models.user import User
import allure


class RegistrationPage(WebPage):

    # Define wrapped Playwright Elements
    def title(self): return el(self.page, 'h1')
    def login_link(self): return el(self.page, 'text="Have an account?"')
    def username_filed(self): return el(self.page, 'input[placeholder="Username"]')
    def email_filed(self): return el(self.page, 'input[placeholder="Email"]')
    def password_field(self): return el(self.page, 'input[placeholder="Password"]')
    def submit_button(self): return el(self.page, 'button[type="submit"]')
    def error_message(self): return el(self.page, '.error-messages')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    @allure.step("Open Login Page")
    def open(self):
        self.page.goto("%s/#/register" % self.base_url, waitUntil="load")
        return self

    @allure.step("Register with: {1}")
    def register_with(self, user: User):
        self.username_filed().shouldBeVisible().val(user.username)
        self.email_filed().val(user.email)
        self.password_field().val(user.password)
        self.submit_button().click()
        return MainPage(self.base_url, self.page)
