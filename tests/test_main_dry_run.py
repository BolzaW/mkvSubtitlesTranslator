import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main

class TestMainDryRun(unittest.TestCase):

    def test_main_mkv_only(self):
        main.data_path = "/data/mkv"
        main.is_dry_run = True

        main.main()

        # TODO vérifier la liste des fichiers
        # TODO vérifier le nombre de piste des fichiers traduits


