import unittest
from unittest import mock

from main import *


class MyTestCase(unittest.TestCase):
    def test_parm_none(self):
        self.assertEqual(main(), TypeError)

    def test_read_path_none(self):
        self.assertEqual(read_path(), IndexError)

    def test_subWord_none(self):
        orig_path = ""
        copy_path = ""
        result_path = ""
        loc = locals()
        self.assertEqual(subWord(orig_path, loc), FileNotFoundError)

    def test_subWord(self):
        orig_path = "text/orig.txt"
        copy_path = ""
        result_path = ""
        loc = locals()
        self.assertEqual(type(subWord(orig_path, loc)), list)

    def test_getSimhash(self):
        orig_path = "text/orig.txt"
        copy_path = ""
        result_path = ""
        loc = locals()
        key_word = subWord(orig_path, loc)
        simhash = getSimhash(key_word)
        for i in simhash:
            self.assertIn(i, ('0', '1'))

    def test_get_similarity(self):
        orig_path = "text/orig.txt"
        copy_path = "text/orig_0.8_add.txt"
        result_path = ""
        loc = locals()
        orig_simhash = getSimhash(subWord(orig_path, loc))
        copy_simhash = getSimhash(subWord(copy_path, loc))
        similarity = get_similarity(orig_simhash, copy_simhash)
        self.assertTrue(0 < similarity < 1)

    def test_output_result_none(self):
        result_path = ""
        result = output_result(result_path, 0.8)
        self.assertEqual(result, (FileNotFoundError, PermissionError))

    def test_output_result(self):
        result_path = "text/test_result.txt"
        result = output_result(result_path, 0.8)
        self.assertEqual(result, None)

    def test_process(self):
        orig_path = "text/orig.txt"
        copy_path = "text/orig_0.8_add.txt"
        result_path = "text/test_result.txt"
        loc = locals()
        self.assertIsNone(process(orig_path, copy_path, result_path, loc))

    def test_process_none(self):
        orig_path = ""
        copy_path = ""
        result_path = ""
        loc = locals()
        self.assertIsNone(process(orig_path, copy_path, result_path, loc))

    @mock.patch("main.read_path")
    def test_main(self, mock_send_cmd):
        mock_send_cmd.return_value = ('text/orig.txt', 'text/orig_0.8_add.txt', 'text/test_result.txt')
        self.assertEqual(main(), None)


if __name__ == '__main__':
    unittest.main()
