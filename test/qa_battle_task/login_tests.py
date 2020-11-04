import pytest
from playwright.sync_api import Page
from playwright.sync_api import Dialog
import time


@pytest.mark.only_browser("chromium")
def test_should_login_to_application(page: Page):
    base_url = 'http://127.0.0.1:8080/'
    page.context.clearCookies()
    page.goto(base_url)
    page.waitForSelector("//*[@id='loginInput']", state="visible")
    page.click('//*[@id="loginInput"]/..')
    page.type('//*[@id="loginInput"]', 'test', delay=10)
    page.click('//*[@id="passwordInput"]/..')
    page.type('//*[@id="passwordInput"]', 'test', delay=10)

    def accept_dialog(dialog: Dialog):
        if "Are you" in dialog.message:
            time.sleep(1)
            dialog.accept()
        else:
            time.sleep(1)
            dialog.accept()

    page.on("dialog", lambda dialog: accept_dialog(dialog))

    # page.evaluate('''()=> {
    #     alert("This message is inside an alert box")
    # }''')

    page.hover("text='Hover me faster!\n            '")
    page.waitForSelector('img[src="sign.png"]', timeout=11000, state="visible").click()
    page.waitForSelector('#loader')
    page.waitForSelector('#avatar', state="visible")
    time.sleep(1)

    # with page.expect_dialog() as dialog:
    #     page.click('img[src="sign.png"]', delay=100)
    #     assert dialog.value.message == "Are you sure you want to login?"
    #     dialog.value.accept()

    # with page.expect_event("dialog", timeout=2000) as popup:
    #     page.click('img[src="sign.png"]')
    #     popup.value.accept()
    # assert popup.value
    # assert popup.value.message == "Are you sure you want to login?"
