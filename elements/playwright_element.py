from playwright.sync_api import Page, ElementHandle

s: ElementHandle = lambda page, css: page.querySelector(css)
ss: ElementHandle = lambda page, css: page.querySelectorAll(css)

el = lambda page, css: PlaywrightElement(page, css)


class PlaywrightElement:

    def __init__(self, page: Page, css):
        self.page = page
        self.selector = css
        self.element_handle: ElementHandle = self.page.querySelector(css)

    def setValue(self, text):
        self.element_handle.fill(text)
        return self

    def val(self, text):
        self.element_handle.fill(text)
        return self

    def sendKeys(self, text, delay=0):
        self.page.waitForSelector(self.selector, state="visible")
        self.element_handle.type(text, delay=delay)
        return self

    def click(self):
        self.page.waitForSelector(self.selector, state="visible")
        self.page.click(self.selector)
        return self

    def shouldBeVisible(self):
        self.page.waitForSelector(self.selector, state="visible")
        return self

    def isEnabled(self):
        if not self.page.evaluate('''(el) => { return el.disabled }''', arg=self.element_handle):
            return True

    def value(self):
        return self.page.evaluate('''(el) => { return el.value }''', arg=self.element_handle)

    def pressTab(self):
        self.page.keyboard.press('Tab')
        return self

    def pressEnter(self):
        self.page.keyboard.press('Enter')
        return self

    def innerText(self):
        return self.page.waitForSelector(self.selector, state="visible").innerText()

    def scrollIntoView(self):
        self.page.evalOnSelector(self.selector, '''(el) => { el.scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"nearest\"}); }''')
        return self


class PlaywrightElements:

    def __init__(self, page: Page, css):
        self.page = page
        self.selector = css
        self.elements: typing.List[ElementHandle] = self.page.querySelectorAll(css)

    def size(self):
        len(self.elements)
