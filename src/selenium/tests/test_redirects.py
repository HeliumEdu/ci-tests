__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.6.4"

import os
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.seleniumtestcase import SeleniumTestCase


class TestSeleniumRedirects(SeleniumTestCase):
    def test_support_redirect(self):
        info = self.get_info()

        self.driver.get(os.path.join(self.app_host, 'support'))
        # The /support URL redirects to an external portal
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("HeliumEdu/platform Wiki")
        )
        self.assertEqual(info['support_url'], self.driver.current_url.strip('/'))

    def test_docs_redirect(self):
        self.driver.get(os.path.join(self.app_host, 'docs'))
        # The /docs URL redirects to the API /docs page
        WebDriverWait(self.driver, 10).until(
            EC.title_is("Helium API Documentation")
        )
        self.assertEqual(os.path.join(self.api_host, 'docs'), self.driver.current_url.strip('/'))

    def test_status_redirect(self):
        start_url = os.path.join(self.app_host, 'status')
        self.driver.get(start_url)
        # The /status URL redirects to the API /status page
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.current_url != start_url
        )
        self.assertEqual(os.path.join(self.api_host, 'status'), self.driver.current_url.strip('/'))


if __name__ == '__main__':
    unittest.main()
