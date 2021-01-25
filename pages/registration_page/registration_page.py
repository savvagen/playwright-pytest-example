from pages.web_elements import *
from pages.web_page import WebPage
from pages.main_page.main_page import MainPage
from models.user import User
import allure


class RegistrationPage(WebPage):

    # Define wrapped Playwright Elements
    def title(self)-> WebElement: return el(self.page, selector='h1')
    def login_link(self)-> WebElement: return el(self.page, selector='text="Have an account?"')
    def username_filed(self)-> WebElement: return el(self.page, selector='input[placeholder="Username"]')
    def email_filed(self)-> WebElement: return el(self.page, selector='input[placeholder="Email"]')
    def password_field(self)-> WebElement: return el(self.page, selector='input[placeholder="Password"]')
    def submit_button(self)-> WebElement: return el(self.page, selector='button[type="submit"]')
    def error_message(self)-> WebElement: return el(self.page, selector='.error-messages')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    @allure.step("Open Login Page")
    def open(self):
        self.page.goto("%s/#/register" % self.base_url, wait_until="load")
        return self

    @allure.step("Register with: {1}")
    def register_with(self, user: User):
        self.username_filed().should_be_visible().val(user.username)
        self.email_filed().val(user.email)
        self.password_field().val(user.password)
        self.submit_button().click()
        return MainPage(self.base_url, self.page)
