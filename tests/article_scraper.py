import logging
import os
import unittest
from unittest.mock import MagicMock

from bs4 import BeautifulSoup

from assets.article_scraper import Article


logging.basicConfig(level=logging.DEBUG)


class ArticleScaperTests(unittest.TestCase):

    def setUp(self) -> None:
        logging.info(f"Setting Up - {self._testMethodName}")
        self._root = os.path.dirname(__file__)
        self._example_path = os.path.join(self._root, "assets", "example.html")
        self.scraper = Article(self._example_path)
        return super().setUp()

    def tearDown(self) -> None:
        # Destroy or clean up after running tests
        logging.info("Tearing Down")
        return super().tearDown()

    def test_scrape_title(self):
        """Scrape the title from our test asset and assert that its working as intended"""
        result = self.scraper.scrape_title()
        expected = "Gregor paul: women showing the men how it's done at the rugby world cup"
        self.assertEqual(result, expected)

    def test_init_loads_files(self):
        """
        Pass in a file path and check that it loads files.
        """
        with open(self._example_path, 'r') as file:
            expected = BeautifulSoup(file, "lxml")

        self.assertIsInstance(self.scraper._html, BeautifulSoup, "Expected to load html from example file.")
        self.assertEqual(self.scraper._html, expected)
        self.assertIsNone(self.scraper._article_text)
        self.assertIsNone(self.scraper._article_title)
        self.assertEqual(self.scraper._text_list, [])
        self.assertIsNone(self.scraper._article_image)

    def test_init_loads_non_existent_file(self):
        """
        Pass in a file path with a  non-exitent file and confirm it throws an error.
        """
        fake_path = os.path.join(self._root, "assets", "fake.html")

        with self.assertRaises(FileNotFoundError) as error_context:
            self.scraper = Article(fake_path)

            actual_error_msg = str(error_context.exception)
            expected_error_msg = "[Errno 2] No such file or directory: '/home/mustard/repos/nzherald_webscraper/tests/assets/fake.html'"

            self.assertEqual(actual_error_msg, expected_error_msg)



    # def test_load_file(self):
    #   pass

