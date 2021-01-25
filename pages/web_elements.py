from playwright.sync_api import Page, ElementHandle
from typing import List
import logging
logger = logging.getLogger("test")



s = lambda page, selector: page.query_selector(selector)
ss = lambda page, selector: page.query_selector_all(selector)


'''
Lazy Element Functions
-----------------------------
This functions returns wrapped elements in the moment
when it is called in the page object.
usage example:

class MyPageObject:
    # 1. Returns wrapped element by slector value
    def my_element(self): return el(self.page, selector='css=*[type="email"]') 
    
    # 2. Returns wrapped element by element value
    def my_element(self): return el(self.page, el=<element_handle>) 
    
    # 3. Returns elements_collection object which keeps the list of elements
    # and introduces interface for working with elements collections(size, index, texts, sorting, etc..)
    def my_element_collection(self): return els(self.page, selector='.my-container .article') 

'''
el = lambda page, selector=None, element=None: WebElement(page, selector, element)
els = lambda page, selector: WebElements(page, selector)
elc = lambda page, elements, element_container: WebElementsCollection(page, elements, element_container)


class WebElement:

    def __init__(self, page: Page,
                 selector: str = None,
                 element: ElementHandle = None):
        self.page = page
        if selector is not None and element is None:
            self.selector = selector
            self.element_handle: ElementHandle = self.page.query_selector(selector)
        elif element is not None and selector is None:
            self.selector = None
            self.element_handle: ElementHandle = element
        else:
            raise Exception(f"Element or Selector is not defined. Please enter arguments: 'selector' or 'element'  {str(type(selector))} ; {str(type(element))}")

    def set_value(self, text):
        if self.selector is None:
            self.element_handle.fill(text)
        else:
            self.page.fill(self.selector, text)
        return self

    def val(self, text):
        self.set_value(text)
        return self

    def send_keys(self, text, delay=10):
        if self.selector is None:
            self.element_handle.wait_for_element_state(state="visible")
            self.element_handle.type(text, delay=delay)
        else:
            self.page.wait_for_selector(self.selector, state="visible")
            self.page.type(self.selector, text, delay=delay)
        return self

    def click(self):
        if self.selector is None:
            self.element_handle.click()
        else:
            self.page.click(self.selector)
        return self

    def should_be_visible(self):
        if self.selector is None:
            self.element_handle.wait_for_element_state(state="visible")
        else:
            self.page.wait_for_selector(self.selector, state="visible")
        return self

    def should_be_hidden(self):
        if self.selector is None:
            self.element_handle.wait_for_element_state(state="hidden")
        else:
            self.page.wait_for_selector(self.selector, state="hidden")
        return self

    def is_enabled(self):
        # if not self.page.evaluate('''(el) => { return el.disabled }''', arg=self.element_handle):
        #     return True
        if self.selector is None:
            return self.element_handle.is_enabled()
        else:
            return self.page.is_enabled(self.selector)

    def is_visible(self):
        if self.selector is None:
            return self.element_handle.is_visible()
        else:
            return self.page.is_visible(self.selector)

    def is_displayed(self):
        if self.selector is None:
            return self.element_handle.is_disabled()
        else:
            return self.page.is_disabled(self.selector)

    def is_checked(self):
        if self.selector is None:
            return self.element_handle.is_checked()
        else:
            return self.page.is_checked(self.selector)

    def value(self):
        if self.selector is None:
            return self.element_handle.evaluate('''(el) => { return el.value }''')
        else:
            return self.page.evaluate('''(el) => { return el.value }''', arg=self.element_handle)

    def press_tab(self):
        self.page.keyboard.press('Tab')
        return self

    def press_enter(self):
        self.page.keyboard.press('Enter')
        return self

    def inner_text(self):
        if self.selector is None:
            self.element_handle.wait_for_element_state(state="visible")
            return self.element_handle.inner_text()
        else:
            self.page.wait_for_selector(self.selector, state="visible")
            return self.page.inner_text(self.selector)

    def scroll_into_view(self):
        if self.selector is None:
            return self.element_handle.evaluate('''el => { el.scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"nearest\"}); }''')
        else:
            self.page.eval_on_selector(self.selector, '''(el) => { el.scrollIntoView({behavior: \"auto\", block: \"center\", inline: \"nearest\"}); }''')
        return self


class WebElements:

    def __init__(self, page: Page, selector: str):
        self.page = page
        self.selector = selector
        self.elements: List[ElementHandle] = self.page.query_selector_all(selector)

    def size(self):
        return len(self.elements)

    def get(self, index):
        return self.elements[index]

    def get_texts(self):
        texts = self.page.eval_on_selector_all(self.selector, '''
                (elems, min) => {
                    return elems.map(function(el) {
                        return el.textContent    //.toUpperCase()
                    });     //.join(", ");
                }''')
        return texts


class WebElementsCollection:

    def __init__(self, page: Page, elements: List[ElementHandle], container_class):
        self.page = page
        self.elements: List[ElementHandle] = elements
        self.container_class = container_class

    def size(self):
        return len(self.elements)

    def get(self, index):
        # logger.info(self.obj_class) # expected output: <class 'pages.main_page.main_page.Article'>
        return self.container_class(page=self.page, element=self.elements[index])

    def get_inner_texts(self):
        def el_text(el: ElementHandle):
            return el.inner_text()
        texts = list(map(el_text, self.elements))
        return texts




