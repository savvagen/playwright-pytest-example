from pages.web_page import WebPage
from pages.web_elements import *
from pages.article_page.article_page import ArticlePage
from models.article import Article
import allure


class EditorPage(WebPage):

    def title_field(self)-> WebElement: return el(self.page, selector='input[placeholder="Article Title"]')
    def subject_field(self)-> WebElement: return el(self.page, selector='input[placeholder="What\'s this article about?"]')
    def body_field(self)-> WebElement: return el(self.page, selector='textarea[placeholder="Write your article (in markdown)"]')
    def publish_button(self)-> WebElement: return el(self.page, selector='text="Publish Article"')
    def tags_field(self)-> WebElement: return el(self.page, selector='input[placeholder="Enter tags"]')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        self.base_url = base_url

    @allure.step("Open Editor Page")
    def open(self):
        self.page.goto("%s/#/editor" % self.base_url, wait_until="load")
        return self

    @allure.step("Publish article: {article.title}")
    def publish_article(self, article: Article):
        self.publish_button().should_be_visible()
        self.title_field().set_value(article.title)
        self.subject_field().set_value(article.subject)
        self.body_field().set_value(article.body)
        self.tags_field().scroll_into_view().set_value(article.tags)
        self.publish_button().click()
        return ArticlePage(self.base_url, None, self.page)
