import unittest
import json
from django.test import Client
from webhookmq import settings
from webhookmq.util.get_message import get_message
from webhookmq.util import randomstring


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.nested = {
            "first": "one",
            "second": "two",
            "nested": {
                "cool": 1,
                "beans": 2
            }
        }
        self.json = json.dumps(self.nested)
        self.flat = {
            "so": "one",
            "very": "two",
            "flat": '1',
            "structure": '2'
        }

    def post_json(self, path, contents=None):
        return self.client.post(path, contents, content_type='application/json')

    def test_nested_json_post(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.post_json(path, self.json)
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(self.nested, response_dict)

    def test_queue_contents_after_nested_json_post(self):
        queue_name = randomstring.id_generator()
        path = '/{}/{}'.format(settings.PATH_PREFIX, queue_name)
        response = self.post_json(path, self.json)
        self.assertEqual(response.status_code, 200)
        queue_message = get_message(settings.MQ_URI, queue_name)
        self.assertEqual(self.nested, queue_message)

    def test_flat_multipart_post(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.post(path, self.flat)
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(self.flat, response_dict)

    def test_queue_contents_after_flat_multipart_post(self):
        queue_name = randomstring.id_generator()
        path = '/{}/{}'.format(settings.PATH_PREFIX, queue_name)
        response = self.client.post(path, self.flat)
        self.assertEqual(response.status_code, 200)
        queue_message = get_message(settings.MQ_URI, queue_name)
        self.assertEqual(self.flat, queue_message)

    def test_empty_post_is_invalid(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.post_json(path)
        self.assertEqual(response.status_code, 400)

    def test_post_to_wrong_path_is_not_found(self):
        path = '/not_{}/queue'.format(settings.PATH_PREFIX)
        response = self.post_json(path, self.json)
        self.assertEqual(response.status_code, 404)

    def test_get_is_wrong_method(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.get(path, self.nested)
        self.assertEqual(response.status_code, 405)

    def test_put_is_wrong_method(self):
        path = '/{}/queue'.format(settings.PATH_PREFIX)
        response = self.client.put(path, self.json)
        self.assertEqual(response.status_code, 405)
