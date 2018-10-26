import unittest
import jericho_config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class JerichoTest(unittest.TestCase):
    def setUp(self):
        if jericho_config.cfg().has_section and jericho_config.cfg().getboolean("Basic", "UseSystemChrome", fallback=False):
            self.browser = webdriver.Chrome('lib/chromedriver')
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
            chrome_options.binary_location = "/tmp/chrome/chrome"
            self.browser = webdriver.Chrome('/tmp/lib/chrome/chromedriver', options=chrome_options)
        self.addCleanup(self.browser.quit)