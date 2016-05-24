import json
from witches.utils.custom_exceptions import WrongValueError
from witches.utils.util import get_sanitized_int, get_sanitized_string_int, sanitize_scene_path

__author__ = 'yoshi.miyamoto'

from witches.master import get_books_list_from_scenetable
import datetime
from django.utils import unittest
from django.test.client import Client
from django.core.cache import cache


now = datetime.datetime.utcnow().replace(tzinfo=None)


class ModelsTestCase(unittest.TestCase):

    def test_http_master(self):
        cache.clear()
        c = Client()
        r = c.get('/witches/master/get_all_master/0')
        self.assertEqual(r.status_code, 200, 'getting all master data failed')

    def test_get_books_list_from_scenetable(self):

        unlock_book_list = get_books_list_from_scenetable()

        self.assertEqual(unlock_book_list.__len__(), 20, 'unlock book list should be 20 but got ' + str(unlock_book_list.__len__()))
        self.assertEqual(unlock_book_list['Prologue/Prologue/Goodbyes'], '54da8a3e6f983f60ee01f779',
                         'book id should be 54da8a3e6f983f60ee01f779 but got ' + str(unlock_book_list['Prologue/Prologue/Goodbyes']))

    def test_sanitize_int_str(self):
        supposed_to_be_int = '1.0'
        expected_int = get_sanitized_int(supposed_to_be_int, 'testtable', 'testcolumn')
        self.assertEqual(expected_int, 1, 'result should be 1 but got ' + str(expected_int))

    def test_sanitize_int_float(self):
        supposed_to_be_int = 1.1
        expected_int = get_sanitized_int(supposed_to_be_int, 'testtable', 'testcolumn')
        self.assertEqual(expected_int, 1, 'result should be 1 but got ' + str(expected_int))

    def test_sanitize_int(self):
        supposed_to_be_int = 1
        expected_int = get_sanitized_int(supposed_to_be_int, 'testtable', 'testcolumn')
        self.assertEqual(expected_int, 1, 'result should be 1 but got ' + str(expected_int))

    def test_sanitize_int_wrong_value(self):
        supposed_to_be_int = '12abc'
        try:
            get_sanitized_int(supposed_to_be_int, 'testtable', 'testcolumn')
        except WrongValueError as e:
            self.assertEqual(str(e), 'wrong value: 12abc in column[testcolumn] in table[testtable]', 'result should be "wrong value: 12abc" but got ' + str(e))

    def test_sanitize_str_int_str(self):
        supposed_to_be_int = '1.0'
        expected_int = get_sanitized_string_int(supposed_to_be_int)
        self.assertEqual(expected_int, '1', 'result should be "1" but got ' + str(expected_int))

    def test_sanitize_str_int(self):
        supposed_to_be_int = 1
        expected_int = get_sanitized_string_int(supposed_to_be_int)
        self.assertEqual(expected_int, '1', 'result should be "1" but got ' + str(expected_int))

    def test_sanitize_str_int_float(self):
        supposed_to_be_int = 1.1
        expected_int = get_sanitized_string_int(supposed_to_be_int)
        self.assertEqual(expected_int, '1', 'result should be "1" but got ' + str(expected_int))

    def test_sanitize_str_int_alpha_numeric(self):
        supposed_to_be_alphanum = '12abc'
        expected_alphanum = get_sanitized_string_int(supposed_to_be_alphanum)
        self.assertEqual(expected_alphanum, '12abc', 'result should be "12abc" but got ' + str(expected_alphanum))

    def test_sanitize_str_int_list(self):
        supposed_to_be_alphanum = '[12abc]'
        expected_alphanum = get_sanitized_string_int(supposed_to_be_alphanum)
        self.assertEqual(expected_alphanum, '[12abc]', 'result should be "[12abc]" but got ' + str(expected_alphanum))

    def test_sanitize_str_int_dict(self):
        supposed_to_be_alphanum = '{12abc: 100.00}'
        expected_alphanum = get_sanitized_string_int(supposed_to_be_alphanum)
        self.assertEqual(expected_alphanum, '{12abc: 100.00}', 'result should be "{12abc: 100.00}" but got ' + str(expected_alphanum))

    def test_sanitize_scene_path(self):
        scene_path = 'Nik-Ana Main Story/NA Germany/White Noise '
        clean_scene_path = sanitize_scene_path(scene_path)
        self.assertEqual(clean_scene_path, 'Nik-Ana Main Story/NA Germany/White Noise', 'result should be "scene" but got ' + str(clean_scene_path))

    def test_ping(self):
        c = Client()
        r = c.get('/witches/ping/1')
        disc = json.loads(r.content)
        self.assertEqual(disc['status'], 'success', 'status should be success but got ' + disc['status'])

