from playwright import sync_playwright
from playwright.sync_api import Request
from pages.login_page.login_page import LoginPage
from models.user import User
from pages.main_page.main_page import MainPage
from test.test_base import *


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.newPage()

    login_page = LoginPage(base_url, page)
    login_page.open()


    def log_and_continue_request(route, request: Request):
        print(request.url)
        print(request.postData)
        route.continue_()
    page.route('**', lambda route, request: log_and_continue_request(route, request))

    # login_page.login("%s@gmail.com" % username, password)
    #
    # print("======||======= Auth Response:")
    # auth_resp: Response = page.waitForResponse("**/api/users/login")
    # print(auth_resp.url)
    # print(auth_resp.body())

    with page.expect_response("**/api/users/login") as resp:
        login_page.login("%s@gmail.com" % username, password)
    auth_resp = resp.value
    import json
    user: User = json.loads(auth_resp.body())
    print(str(user))
    print(str(user["user"]['username']))
    print(str(user["user"]['token']))

    assert MainPage(base_url, page).account_button(username).innerText() == username

    page.goto("%s/#/" % base_url)
    print(page.context.cookies())

    browser.close()


# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.newPage()
#
#     def print_requests(request: Request):
#         print(request.url)
#
#     page.on("request", lambda request: print_requests(request))
#
#     def filter_requests(route: Route, request: Request):
#         # 1. Replace all images on parrot image
#         if route.request.resourceType != 'image':
#             return route.continue_()
#         else:
#             lorem_flickr = "https://loremflickr.com"
#             route.fulfill(status=301, headers={'location': f"{lorem_flickr}/320/240/parrot"})
#         # 2. Filter advertisement
#         # if request.frame.parentFrame:
#         #     route.abort()
#         # else:
#         #     route.continue_()
#
#     page.route('**/*', lambda route, request: filter_requests(route, request))
#
#     page.goto("https://www.theverge.com")
#     time.sleep(4)
#     browser.close()
