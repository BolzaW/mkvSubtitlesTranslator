
import unittest
import os
import sys
import pysrt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from translate_srt import translate_srt_file, cleanup_subtitles

class TestTranslateApi(unittest.TestCase):
    srt_file_familier = "/app/test_data/trad/familier.srt"
    srt_file_soutenu = "/app/test_data/trad/soutenu.srt"
    output_file_familier = "/app/test_data/trad/familier_trad.srt"
    output_file_soutenu = "/app/test_data/trad/soutenu_trad.srt"

    def tearDown(self):
        # A commenter pour voir la traduction proposer par deepL
        if os.path.exists(self.output_file_familier):
            os.remove(self.output_file_familier)
        if os.path.exists(self.output_file_soutenu):
            os.remove(self.output_file_soutenu)

    def test_translate_with_deepl_familier(self):
        """Teste la traduction avec deepL (Attention consomme des caractères)"""
        list_api_keys = [key.strip() for key in os.getenv("DEEPL_API_KEYS", "").split(",") if key.strip()]
        translate_srt_file(self.srt_file_familier,self.output_file_familier, False, list_api_keys)

    def test_translate_with_deepl_soutenu(self):
        """Teste la traduction avec deepL (Attention consomme des caractères)"""
        list_api_keys = [key.strip() for key in os.getenv("DEEPL_API_KEYS", "").split(",") if key.strip()]
        translate_srt_file(self.srt_file_soutenu,self.output_file_soutenu, False, list_api_keys)

if __name__ == '__main__':
    unittest.main()
