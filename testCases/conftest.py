import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

@pytest.fixture()
def setup(browser):
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("-private")
        driver = webdriver.Firefox(options=firefox_options)
    elif browser == "edge":
        edge_options = EdgeOptions()
        edge_options.use_in_private_mode = True
        driver = webdriver.Edge(options=edge_options)
    else:
        raise ValueError("Browser not Supported")

    driver.delete_all_cookies()
    return driver


def pytest_addoption(parser):
    parser.addoption("--browser")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")