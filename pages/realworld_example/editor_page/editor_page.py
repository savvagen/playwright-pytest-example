from pages.web_page import WebPage
from playwright.sync_api import Page
from elements.playwright_element import *
from pages.realworld_example.article_page.article_page import ArticlePage
import allure


class EditorPage(WebPage):

    def title_field(self): return el(self.page, 'input[placeholder="Article Title"]')
    def subject_field(self): return el(self.page, 'input[placeholder="What\'s this article about?"]')
    def body_field(self): return el(self.page, 'textarea[placeholder="Write your article (in markdown)"]')
    def publish_button(self): return el(self.page, 'text="Publish Article"')
    def tags_field(self): return el(self.page, 'input[placeholder="Enter tags"]')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    @allure.step("Open Editor Page")
    def open(self):
        self.page.goto("%s/#/editor" % self.base_url, waitUntil="load")
        return self

    @allure.step("Publish article: {title}")
    def publish_article(self, title, subject, body, tags="test"):
        self.publish_button().shouldBeVisible()
        self.title_field().setValue(title)
        self.subject_field().setValue(subject)
        self.body_field().setValue(body)
        self.tags_field().scrollIntoView().setValue(tags)
        self.publish_button().click()
        # Extract Article ID from url
        # url = self.page.url
        # path = url.split("article/")[1]
        # article_id = path.split("?")[0]
        return ArticlePage(self.base_url, None, self.page)
