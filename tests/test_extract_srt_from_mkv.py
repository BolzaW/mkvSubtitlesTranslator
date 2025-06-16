import unittest
import pysrt
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from extract_srt_from_mkv import extract_subtitle

class TestExtractSubtitles(unittest.TestCase):
    mkv_test_file_path = "/app/test_data/mkv_to_srt/test.mkv"
    srt_result_file_path = "/app/test_data/mkv_to_srt/test.srt"
    srt_specified_result_file_path = "/app/test_data/mkv_to_srt/test_specified.srt"
    srt_expected_file_path = "/app/test_data/mkv_to_srt/expected.srt"

    def tearDown(self):
        if os.path.exists(self.srt_result_file_path):
            os.remove(self.srt_result_file_path)
        if os.path.exists(self.srt_specified_result_file_path):
            os.remove(self.srt_specified_result_file_path)

    def test_extract_with_one_arg(self):
        """Teste la fonction d'exctraction avec un argument"""
        extract_subtitle(self.mkv_test_file_path)
        self.assertTrue(os.path.isfile(self.srt_result_file_path), "Le fichier test.srt devrait exister")
        result = pysrt.open(self.srt_result_file_path, encoding='utf-8')
        expected = pysrt.open(self.srt_expected_file_path, encoding='utf-8')
        self.assertEqual(result, expected, "Le fichier test.srt devrait être égal à expected.srt")

    def test_extract_with_two_arg(self):
        """Teste la fonction d'exctraction avec deux arguments"""
        extract_subtitle(self.mkv_test_file_path, self.srt_specified_result_file_path)
        self.assertTrue(os.path.isfile(self.srt_specified_result_file_path), "Le fichier test_specified.srt devrait exister")
        result = pysrt.open(self.srt_specified_result_file_path, encoding='utf-8')
        expected = pysrt.open(self.srt_expected_file_path, encoding='utf-8')
        self.assertEqual(result, expected, "Le fichier test_specified.srt devrait être égal à expected.srt")

    def test_extract_with_no_file(self):
        """Teste la fonction d'exctraction avec un fichier introuvable"""
        with self.assertRaises(FileNotFoundError):
            extract_subtitle("/app/test_data/mkv_to_srt/unknown.mkv")
    
    def test_extract_with_bad_mp4_file(self):
        """Teste la fonction d'exctraction avec un fichier du mauvais type"""
        with self.assertRaises(ValueError):
             extract_subtitle("/app/test_data/mkv_to_srt/test.mp4")
    
    def test_extract_with_no_subtitle_in_file(self):
        """Teste la fonction d'exctraction avec un fichier sans sous-titre"""
        with self.assertRaises(ValueError):
             extract_subtitle("/app/test_data/mkv_to_srt/no_sub.mkv")

    def test_extract_with_bad_mkv_file(self):
        """Teste la fonction d'exctraction avec un mauvais fichier mkv"""
        with self.assertRaises(RuntimeError):
             extract_subtitle("/app/test_data/mkv_to_srt/bad.mkv")

if __name__ == '__main__':
    unittest.main()

    