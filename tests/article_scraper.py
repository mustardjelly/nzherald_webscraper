from decimal import DivisionByZero
import logging
import os
import unittest
from unittest.mock import MagicMock, Mock, patch

from bs4 import BeautifulSoup

from assets.article_scraper import Article


logging.basicConfig(level=logging.DEBUG)


class ArticleScaper(unittest.TestCase):

    def setUp(self) -> None:
        logging.debug(f"Setting Up - {self._testMethodName}")
        self._root = os.path.dirname(__file__)
        self._example_path = os.path.join(self._root, "assets", "example.html")
        self.scraper = Article(self._example_path)
        return super().setUp()

    def tearDown(self) -> None:
        logging.debug("Tearing Down")
        return super().tearDown()

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

    def test_scrape_title(self):
        """Scrape the title from our test asset and assert that its working as intended"""
        result = self.scraper.scrape_title()
        expected = "Gregor paul: women showing the men how it's done at the rugby world cup"
        self.assertEqual(result, expected)

    def test_mocking(self):
        mock = MagicMock(return_value="Ran!")
        self.scraper.run = mock
        self.scraper.run("1")
        self.scraper.run("2")
        self.scraper.run("3")

        self.assertEqual(mock.call_count, 3)

    def test_mocking2(self):
        mock = Mock(side_effect=DivisionByZero('foo'))
        self.scraper.run = mock
        with self.assertRaises(DivisionByZero):
            self.scraper.run("1")
        
    def test_scrape_image(self):
        # Arrange
        self.scraper.scrape_title()
        self.scraper.scrape_text()

        # Act
        self.scraper.scrape_image()

        # Assert
        self.assertIsNotNone(self.scraper.article_image)
        # Check the contents of article_image
        
    def test_scrape_image_if_no_1440_does_nothing(self):
        """
        If no 1440 found in img tags, returns nothing
        """
        # Arrange
        self.scraper.scrape_title()
        self.scraper.scrape_text()
        self.scraper._html.find_all = MagicMock(return_value=["1440"])

        # Act
        self.scraper.scrape_image()

        # Assert
        self.assertIsNone(self.scraper.article_image)
        # Check the contents of article_image

    def test_scrape_image_called_out_of_order(self):
        """
        Test calling scrape image out of sequence raises an error.
        """
        with self.assertRaises(TypeError) as cntxt:
            self.scraper.scrape_image()

            actual_error = str(cntxt.exception)
            expected_error = "expected string or bytes-like object"
            self.assertEqual(actual_error, expected_error)
            self.assertIsNone(self.scraper._article_title)

