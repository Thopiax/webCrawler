#!/usr/local/bin/python3

import unittest
from unittest.mock import patch
from requests.exceptions import MissingSchema, ConnectionError
from WebCrawler import *
from WebCrawlerUtil import *

class CrawlerUtilTest(unittest.TestCase):

    # REGEX
    def testRegExForHTTP(self):
        self.assertEqual(get_base_url("http://www.example.com/questions/random"), 
                                         "http://www.example.com")

    def testRegExForHTTPS(self):
        self.assertEqual(get_base_url("https://www.example.com/doc/about"), 
                                         "https://www.example.com")

    def testRegExForSubDomain(self):
        self.assertEqual(get_base_url("http://test.example.com/about/try"), 
                                 "http://test.example.com")

    def testRegExForSubDomain(self):
        self.assertEqual(get_base_url("http://example.com/about/try"), 
                                 "http://example.com")

    def testRegExForAlreadyBaseUrl(self):
        self.assertEqual(get_base_url("http://www.example.com"), 
                                 "http://www.example.com")

    def testExForComposedEnd(self):
        self.assertEqual(get_base_url("http://www.example.co.uk/"), 
                                 "http://www.example.co.uk")

    def testRegExShouldWorkForFileInFolder(self):
        self.assertTrue(is_under_domain("web"))

    def testRegExShouldWorkForFileInOtherFolder(self):
        self.assertTrue(is_under_domain("../../web"))

    def testRegExShouldNotWorkForURL(self):
        self.assertFalse(is_under_domain("https://www.crummy.com/"))

    def testRegExShouldNotWorkForElement(self):
        self.assertFalse(is_under_domain("#element"))

    def testRegExShouldWorkForFileInFolder(self):
        self.assertFalse(is_under_domain("mailto:privacy@test.com"))

class CrawlerControllerTest(unittest.TestCase):

    def testEmptyURLCrawler(self):
        runFailingCrawler("", MissingSchema)

    def testNonExistantURLCrawler(self):
        runFailingCrawler("https://www.test.test/testing/test/exampleasdjfk", ConnectionError)

def runFailingCrawler(url, exc):
    crawler = Crawler(url)
    with self.assertRaises(exc):
        empty_crawler.get_static_assets()

if __name__ == '__main__':
    unittest.main()
