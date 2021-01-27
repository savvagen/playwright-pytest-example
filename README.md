# Playwright Pytest Example Project

![Build Status](https://github.com/savvagen/playwright-pytest-example/workflows/Playwright%20Pytest%20Example/badge.svg)
![Free](https://img.shields.io/badge/free-open--source-green.svg)

##  Last Published results:
<a href="https://savvagen.github.io/playwright-pytest-example"> 
    <img src="https://avatars3.githubusercontent.com/u/5879127?s=200&v=4" width="50" height="50">
    <p>Allure Report on Github Pages
</a>

## Running Tests

Go to test directory: `test`

#### Run Tests in 1 thread
``` 
pytest login_tests.py --headful
```

#### Run Tests in parallel
```
pipenv install pytest-xdist
cd test
pytest login_tests.py registration_tests.py article_tests.py --headful -n 3
```

#### Run With Allure Report in parallel
``` 
cd test
pytest login_tests.py article_tests.py registration_tests.py --headful --alluredir=./allure-results -n 3
allure generate
allure serve allure-results
```

#### Run tests on all browser engines (chromium, firefox, webkit)
```
# Note!!!!
# Make sure that "@pytest.mark.only_browser" decorators are commented under the tests

pytest article_tests.py --browser chromium --browser firefox --browser webkit --headful -n 3
```