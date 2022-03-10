from unittest import TestCase, main, mock
import bs4
import helpers
import mock_data

class TestHelpers(TestCase):

    def test_get_data(self):
        with mock.patch('helpers.requests.get') as mocked_get:
            mocked_get.return_value.content = 'mock_content'
            response = helpers.get_data('url')
            self.assertEqual(response, 'mock_content')
    
    def test_get_zip_link(self):
        data = helpers.get_zip_link(mock_data.bs_mock_object)
        self.assertEqual(data, 'zip_link1.zip')

    def test_create_beautifulSoup_object(self):
        bs = helpers.create_beautifulSoup_object(mock_data.html_data)
        self.assertIsInstance(bs, bs4.element.PageElement)

    def test_extract_data_from_xml(self):
        read_data = mock_data.xml_data
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_open):
            result = helpers.extract_data_from_xml('filename')
            self.assertEqual(result, [['DE000A1R07V3','KFW 1 5/8 01/15/21','DBFTFB','false','EUR', '549300GDPG70E3MBBU98']])
