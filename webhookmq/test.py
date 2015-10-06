import unittest
import json
from django.test import Client
from webhookmq import settings
from webhookmq.util.get_message import get_message
from webhookmq.util import randomstring


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.postdata = {
            "first": "one",
            "second": "two",
            "nested": {
                "cool": 1,
                "beans": 2
            }
        }

    def test_valid_post(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.post(path, self.postdata, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(self.postdata, sort_keys=True), response.content)

    def test_empty_post_is_invalid(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.post(path, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_to_wrong_path_is_not_found(self):
        path = '/not_{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.post(path, self.postdata, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_is_wrong_method(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.get(path, self.postdata, content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_put_is_wrong_method(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.put(path, self.postdata, content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_queue_contents_after_valid_post(self):
        queue_name = randomstring.id_generator()
        path = '/{}/{}'.format(settings.PATH_PREFIX, queue_name)
        response = self.client.post(path, self.postdata, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        queue_message = get_message(settings.MQ_URI, queue_name)
        self.assertEqual(
            json.dumps(self.postdata, sort_keys=True), queue_message, content_type='application/json')
