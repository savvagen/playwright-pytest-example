import requests
from playwright import sync_playwright
from pages.realworld_example.main_page.main_page import MainPage
from pages.realworld_example.login_page.login_page import LoginPage
import time

with sync_playwright() as p:
    base_url = "https://react-redux.realworld.io"

    # 1. Making Login HTTP Request
    headers = {"content-type": "application/json; charset=utf-8"}
    json = '{"user":{"email":"savva.genchevskiy@gmail.com","password":"S.gench19021992"}}'
    resp = requests.post("https://conduit.productionready.io/api/users/login", data=json, headers=headers)
    print(resp.status_code)
    print(resp.content)
    print(resp.cookies.get('__cfduid'))

    # 2. Launch Browser Context
    browser = p.chromium.launch(headless=False)
    page = browser.newPage()

    cookie = {"name": "__cfduid", "value": resp.cookies.get('__cfduid'), "domain": ".productionready.io", "path": "/",
              "httpOnly": True, "sameSite": "Lax"}
    cookies = [cookie]

    # 3. Open Web Page
    main_page = MainPage(base_url, page).open()
    # 4. Set Cookies and put JWT token to Local Storage
    page.evaluate("(t) => { localStorage.setItem('jwt', `${t}`) }", arg=resp.json()['user']['token'])
    page.context.addCookies(cookies)
    st = page.evaluate('''()=> { return localStorage.getItem('jwt')} ''')
    print("Local Storage JWT")
    print(st)
    # 5. Enjoy!!! Reload Page as Logged In User
    main_page.page.reload()
    time.sleep(5)
    page.screenshot(path='main_page.png')

    browser.close()
