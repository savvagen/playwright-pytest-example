import allure
from pages.web_page import WebPage
from pages.web_elements import *


class ArticlePage(WebPage):

    def title(self): return el(self.page, selector='.container > h1')
    def author_link(self): return el(self.page, selector='.author')
    def subject(self): return el(self.page, selector='div[class*="article-content"] h1')
    def publish_button(self): return el(self.page, selector='text="Publish Article"')
    def tags_field(self): return el(self.page, selector='input[placeholder="Enter tags"]')

    def __init__(self, base_url, article_id, page: Page):
        super().__init__(page)
        self.base_url = base_url
        self.article_id = article_id

    @allure.step
    def open(self):
        self.page.goto("%s/#/article/%s" % self.base_url, self.article_id, wait_until="load")
        return self
