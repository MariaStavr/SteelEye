from unittest import TestCase, main, mock
import helpers
import mock_data


class TestHelpers(TestCase):

    def test_get_data(self):
        with mock.patch('helpers.requests.get') as mocked_get:
            mocked_get.return_value.content = 'mock_content'
            response = helpers.get_data()
            self.assertEqual(response, 'mock_content')
    
    def test_get_zip_link(self):
        data = helpers.get_zip_link(mock_data.bs_mock_object)
        self.assertEqual(data, 'zip_link1.zip')
