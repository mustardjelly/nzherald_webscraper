import logging
import unittest
from unittest.mock import MagicMock

from assets.article_scraper import Article


logging.basicConfig(level=logging.DEBUG)


class ArticleScaperTests(unittest.TestCase):

    def setUp(self) -> None:
        # Load our test document
        # Create an Article
        logging.info("Setting Up")
        return super().setUp()

    def tearDown(self) -> None:
        # Destroy or clean up after running tests
        logging.info("Tearing Down")
        return super().tearDown()

    def test_scrape_title(self):
        """Scrape the title from our test asset and assert that its working as intended"""
        self.scraper = Article()
        "ResourceWarning: Enable tracemalloc to get the object allocation traceback"
        pass

    # def test(self):
    #     self.assertFalse(True, "Failing test")

    # def test_load_file(self):
    #   pass

