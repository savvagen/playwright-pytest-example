from unittest import TestCase
from playwright import sync_playwright

base_url = "https://react-redux.realworld.io"


class MyViewTests(TestCase):
    playwright = None
    browser = None

    @classmethod
    def setUpClass(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)

    @classmethod
    def tearDownClass(self):
        self.browser.close()
        self.playwright.stop()

    def test_login(self):
        page = self.browser.newPage()
        page.context.clearCookies()
        page.goto('%s/#/login' % base_url)
        page.fill('input[type="email"]', "savva.genchevskiy@gmail.com")
        page.fill('input[type="password"]', "S.gench19021992")
        page.click('button[type="submit"]')  # page.click('text="Sign in"')
        assert page.innerText('a[href="#@savva.genchevskiy"]') == 'savva.genchevskiy'
        assert "%s/#/" % base_url in page.url
        page.screenshot(path='../logged_in.png')
        page.close()

    # def setUp(self):
    #     self.page = self.browser.newPage()
    #
    # def tearDown(self):
    #     self.page.close()
    #
    # def test_login(self):
    #     self.page.context.clearCookies()
    #     self.page.goto('%s/#/login' % base_url)
    #     self.page.fill('input[type="email"]', "savva.genchevskiy@gmail.com")
    #     self.page.fill('input[type="password"]', "S.gench19021992")
    #     self.page.click('button[type="submit"]')  # page.click('text="Sign in"')
    #     assert self.page.innerText('a[href="#@savva.genchevskiy"]') == 'savva.genchevskiy'
    #     assert "%s/#/" % base_url in self.page.url
    #     self.page.screenshot(path='logged_in.png')
