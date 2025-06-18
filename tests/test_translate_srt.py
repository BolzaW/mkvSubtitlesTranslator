import unittest
import os
import sys
import pysrt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from translate_srt import translate_srt_file, cleanup_subtitles

class TestTranslateSubtitles(unittest.TestCase):
    srt_file_to_clean = "/app/test_data/mkv_to_srt/toclean.srt"
    expected_srt_file = "/app/test_data/mkv_to_srt/clean.srt"
    expected_srt_file_with_songs = "/app/test_data/mkv_to_srt/clean_with_songs.srt"

    def test_cleanup_with_songs(self):
        """Teste le nettoyage de sous titre avec le paramètre clean music à True"""
        subs = pysrt.open(self.srt_file_to_clean, encoding='utf-8')
        clean_subs = cleanup_subtitles(subs, True)
        expected_subs = pysrt.open(self.expected_srt_file, encoding='utf-8')
        self.assertEqual(len(clean_subs), len(expected_subs), "Le fichier nettoyé devrait être aussi long que le fichier attendu")
        for i in range(len(clean_subs)):
            self.assertEqual(clean_subs[i].text, expected_subs[i].text, "Le texte du fichier nettoyé devrait être égal au texte du fichier attendu")

    def test_cleanup_without_songs(self):
        """Teste le nettoyage de sous titre avec le paramètre clean music à False"""
        subs = pysrt.open(self.srt_file_to_clean, encoding='utf-8')
        clean_subs = cleanup_subtitles(subs, False)
        expected_subs = pysrt.open(self.expected_srt_file_with_songs, encoding='utf-8')
        self.assertEqual(len(clean_subs), len(expected_subs), "Le fichier nettoyé devrait être aussi long que le fichier attendu")
        for i in range(len(clean_subs)):
            self.assertEqual(clean_subs[i].text, expected_subs[i].text, "Le texte du fichier nettoyé devrait être égal au texte du fichier attendu")


if __name__ == '__main__':
    unittest.main()
