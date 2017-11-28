import unittest
from scrape import *
from unittest.mock import patch, Mock

class TestMS(unittest.TestCase):

    def setUp(self):
        self.target_url = 'https://www.metal-archives.com/browse/ajax-country/c/SE/json/1'
        self.target_url += '?sEcho=1&iColumns=4&sColumns=&iDisplayStart=0&iDisplayLength=500'
        self.target_url += '&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&iSortCol_0=0'
        self.target_url += '&sSortDir_0=asc&iSortingCols=1&bSortable_0=true&bSortable_1=true'
        self.target_url += '&bSortable_2=true&bSortable_3=false&_=1505682951191'

        self.data = ["<a href='https://www.metal-archives.com/bands/%24ilverdollar/60323'>$ilverdollar</a>",
        "Heavy/Power Metal", "Nyköping", '<span class="active">Active</span>']

        self.soup_obj = "This is a soup object probably idk."

    def test_current_target_url(self):
        self.assertEqual(MetalScraper.current_target_url(1, 0), self.target_url)

    def test_get_total_records(self):
        self.assertGreater(MetalScraper.get_total_records(self.target_url), 0)

    @patch('scrape.MetalScraper')
    def test_json_data(self, Mock):
        mock = Mock()
        mock.get_json_data.return_value = self.data

        self.assertEqual(MetalScraper.get_json_data(self.target_url)["aaData"][0], self.data)

    def test_crawler(self):
        self.assertIsNone(MetalScraper.crawler())

    @patch('scrape.MetalScraper.get_band_attributes', return_value = True)
    def test_get_band_attributes(self, attribute):
        self.assertTrue(attribute(self.soup_obj))

    @patch('scrape.MetalScraper.get_band_disco', return_value = True)
    def test_get_discography(self, entry):
        self.assertTrue(entry(self.soup_obj, 1))

    @patch('scrape.MetalScraper.get_band_members', return_value = True)
    def test_get_band_members(self, band):
        self.assertTrue(band(self.soup_obj, 1))


if __name__ == '__main__':
    unittest.main()
