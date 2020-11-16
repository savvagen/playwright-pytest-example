from unittest import TestCase
from playwright import sync_playwright
from test.realworld_example.test_base import *



class MyViewTests(TestCase):
    playwright = None
    browser = None

    # def setUp(self):
    #     self.page = self.browser.newPage()
    #
    # def tearDown(self):
    #     self.page.close()

    @classmethod
    def setUpClass(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        # Connect to moon cluster
        # self.browser = self.playwright.chromium.connect(timeout=0, wsEndpoint="ws://moon.example.com:4444/playwright/chromium?headless=false")

    @classmethod
    def tearDownClass(self):
        self.browser.close()
        self.playwright.stop()

    def test_login(self):
        page = self.browser.newPage()
        page.context.clearCookies()
        page.goto('%s/#/login' % base_url)
        page.fill('input[type="email"]', "%s@gmail.com" % username)
        page.fill('input[type="password"]', password)
        page.click('button[type="submit"]')  # page.click('text="Sign in"')
        assert page.innerText('a[href="#@%s"]' % username) == username
        assert "%s/#/" % base_url in page.url
        page.screenshot(path='screenshots/logged_in.png')
        page.close()
