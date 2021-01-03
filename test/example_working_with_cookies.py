import requests
from playwright import sync_playwright
from pages.main_page.main_page import MainPage
import time
from test.test_base import *

with sync_playwright() as p:

    # 1. Making Login HTTP Request
    headers = {"content-type": "application/json; charset=utf-8"}
    json = {"user": {"email": username+"@gmail.com", "password": password}}
    resp = requests.post("https://conduit.productionready.io/api/users/login", json=json, headers=headers)
    print(resp.status_code)
    print(resp.content)
    print(resp.cookies.get('__cfduid'))

    # 2. Launch Browser Context
    browser = p.chromium.launch(headless=False)
    page = browser.newPage()

    cookie = {"name": "__cfduid",
              "value": resp.cookies.get('__cfduid'),
              "domain": ".productionready.io",
              "path": "/",
              "httpOnly": True, "sameSite": "Lax"}

    # 3. Open Web Page
    main_page = MainPage(base_url, page).open()

    # 4. Set Cookies and put JWT token to Local Storage
    page.evaluate("(t) => { localStorage.setItem('jwt', `${t}`) }", arg=resp.json()['user']['token'])
    page.context.addCookies([cookie])
    st = page.evaluate('''()=> { return localStorage.getItem('jwt')} ''')
    print("Local Storage JWT")
    print(st)

    # 5. Enjoy!!! Reload Page as Logged In User
    main_page.page.reload()
    time.sleep(5)
    page.screenshot(path='main_page.png')

    browser.close()
