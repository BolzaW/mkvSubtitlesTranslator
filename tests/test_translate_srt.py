import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from translate_srt import translate_srt_file

class TestTranslateSubtitles(unittest.TestCase):
    # TODO
    def test(self):
        self.assertTrue