
# Running Tests

Go to test directory: `test/realworld_example`

### Run Tests in 1 thread
``` 
pytest login_tests.py --headful
```

### Run Tests in parallel
```
pipenv install pytest-xdist
cd test/realworld_example
pytest login_tests.py registration_tests.py article_tests.py --headful -n 3
```

### Run With Allure Report in parallel
``` 
cd test/realworld_example
pytest login_tests.py article_tests.py registration_tests.py --headful --alluredir=./allure-results -n 3
allure generate
allure serve allure-results
```