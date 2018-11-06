import unittest
from jericho_config import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os

environment = None

def getenv(test_module):
    return environment[test_module]


def setenv(env):
    environment = env

def loadenv(json_str):
    environment = json.loads(json_str)


def loadenvfile(path):
    return loadenv(open(path))


class JerichoTest(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        if environment is not None:
            self.env = environment[self.__class__.__module__]
        else:
            self.env = {}


    def setUp(self):
        if config.use_system_chrome:
            self.browser = webdriver.Chrome(os.path.join(config.function_root, 'lib/chromedriver'))
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1200x1000')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--no-zygote')
            chrome_options.add_argument('--hide-scrollbars')
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--log-level=0')
            chrome_options.add_argument('--v=99')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--data-path=/tmp/data-path')
            chrome_options.add_argument('--user-data-dir=/tmp/user-data')
            chrome_options.add_argument('--homedir=/tmp')
            chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
            chrome_options.binary_location = config.chromium_dir + "chrome"
            self.browser = webdriver.Chrome(config.chromium_dir + 'chromedriver', options=chrome_options)
        self.addCleanup(self.browser.quit)