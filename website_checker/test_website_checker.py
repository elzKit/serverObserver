import re
from unittest import TestCase

import website_checker


class Test(TestCase):

    def test_check_url_existing_website_no_regexp(self):
        url = 'aiven.io'
        msg = website_checker.check(url)
        # check the presence of expected metrics
        self.assertTrue('timestamp' in msg)
        self.assertTrue('url' in msg)
        self.assertTrue('response_time' in msg)
        self.assertTrue('status_code' in msg)
        self.assertTrue('matched' not in msg)

        self.assertTrue(isinstance(msg['timestamp'], float))
        self.assertTrue(msg['url'] == 'http://aiven.io')
        self.assertEqual(msg['status_code'], '200')

    def test_check_url_existing_website_with_regexp(self):
        url = 'aiven.io'
        regexp = 'L?g in'
        msg = website_checker.check(url, regexp)
        # check the presence of expected metrics
        self.assertTrue('timestamp' in msg)
        self.assertTrue('url' in msg)
        self.assertTrue('response_time' in msg)
        self.assertTrue('status_code' in msg)
        self.assertTrue('matched' in msg)

        self.assertTrue(isinstance(msg['timestamp'], float))
        self.assertTrue(msg['url'] == 'http://aiven.io')
        self.assertEqual(msg['status_code'], '200')
        self.assertTrue(msg['matched'])

    def test_check_url_existing_website_with_compiled_regexp(self):
        url = 'aiven.io'
        regexp = 'L?g in'
        msg = website_checker.check(url, re.compile(regexp))
        # check the presence of expected metrics
        self.assertTrue('timestamp' in msg)
        self.assertTrue('url' in msg)
        self.assertTrue('response_time' in msg)
        self.assertTrue('status_code' in msg)
        self.assertTrue('matched' in msg)

        self.assertTrue(isinstance(msg['timestamp'], float))
        self.assertTrue(msg['url'] == 'http://aiven.io')
        self.assertEqual(msg['status_code'], '200')
        self.assertTrue(msg['matched'])

    def test_check_url_non_existing_website_with_compiled_regexp(self):
        url = 'this_website_does_not_exist.com'
        regexp = 'L?g in'
        msg = website_checker.check(url, re.compile(regexp))
        # check the presence of expected metrics
        self.assertTrue('timestamp' in msg)
        self.assertTrue('url' in msg)
        self.assertFalse('response_time' in msg)
        self.assertFalse('status_code' in msg)
        self.assertFalse('matched' in msg)
        self.assertTrue('error_msg' in msg)

        self.assertTrue(isinstance(msg['timestamp'], float))
        self.assertTrue(msg['url'] == 'http://this_website_does_not_exist.com')
