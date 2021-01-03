from playwright.sync_api import Page, ElementHandle

s: ElementHandle = lambda page, css: page.querySelector(css)
ss: ElementHandle = lambda page, css: page.querySelectorAll(css)

el = lambda page, css: WebElement(page, css)
elh = lambda page, el: WebElementHandle(page, el)
els = lambda page, css: WebElements(page, css)


class WebElement:

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

    def sendKeys(self, text, delay=10):
        self.element_handle.waitForElementState(state="visible").type(text, delay=delay)
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
        self.page.evalOnSelector(self.selector,
                                 '''(el) => { el.scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"nearest\"}); }''')
        return self


class WebElementHandle:

    def __init__(self, page: Page, element_handle: ElementHandle):
        self.page = page
        self.element_handle: ElementHandle = element_handle

    def setValue(self, text):
        self.element_handle.fill(text)
        return self

    def val(self, text):
        self.element_handle.fill(text)
        return self

    def sendKeys(self, text, delay=10):
        self.element_handle.waitForElementState(state="visible").type(text, delay=delay)
        return self

    def click(self):
        self.element_handle.waitForElementState(state="visible").click()
        return self

    def shouldBeVisible(self):
        self.element_handle.waitForElementState(state="visible")
        return self

    def isEnabled(self):
        if not self.page.evaluate('''(el) => { return el.disabled }''', arg=self.element_handle):
            return True

    def value(self):
        return self.page.evaluate('''(el) => { return el.value }''', arg=self.element_handle)

    def pressTab(self):
        self.element_handle.press('Tab')
        return self

    def pressEnter(self):
        self.element_handle.press('Enter')
        return self

    def innerText(self):
        self.element_handle.waitForElementState(state="visible")
        return self.element_handle.innerText()

    def scrollIntoView(self):
        self.page.evaluate('''(el) => { el.scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"nearest\"}); }''', arg=self.element_handle)
        return self




class WebElements:

    def __init__(self, page: Page, css):
        self.page = page
        self.selector = css
        self.elements: typing.List[ElementHandle] = self.page.querySelectorAll(css)

    def size(self):
        return len(self.elements)

    def get(self, index):
        return self.elements[index]

    def get_texts(self):
        texts = self.page.evalOnSelectorAll(self.selector, '''
                (elems, min) => {
                    return elems.map(function(el) {
                        return el.textContent    //.toUpperCase()
                    });     //.join(", ");
                }''')
        return texts
