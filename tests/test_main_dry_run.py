import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main

class TestMainDryRun(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("/data/mkv/test1_vostfr.mkv"):
            os.remove("/data/mkv/test1_vostfr.mkv")
        if os.path.exists("/data/mkv/test2_vostfr.mkv"):
            os.remove("/data/mkv/test2_vostfr.mkv")
        if os.path.exists("/data/mkv/test3_vostfr.mkv"):
            os.remove("/data/mkv/test3_vostfr.mkv")
        if os.path.exists("/data/srt/ambigu.fr.srt"):
            os.remove("/data/srt/ambigu.fr.srt")
        if os.path.exists("/data/srt/familier.fr.srt"):
            os.remove("/data/srt/familier.fr.srt")
        if os.path.exists("/data/srt/soutenu.fr.srt"):
            os.remove("/data/srt/soutenu.fr.srt")


    def test_main_mkv_only(self):
        """Teste la boucle entière du logiciel sur le dossier /data/mkv contenant uniquement des fichiers .mkv"""
        main.data_path = "/data/mkv"
        main.is_dry_run = True

        main.main()

        file_list = os.listdir("/data/mkv")

        print(f"filelist : {file_list}")
        
        self.assertEqual(len(file_list), 6, "Le dossier devrait comporter 6 videos")
        if not "test1.mkv" in file_list :
            self.assertFalse("Le fichier test1.mkv devrait exister")
        if not "test2.mkv" in file_list :
            self.assertFalse("Le fichier test2.mkv devrait exister")
        if not "test3.mkv" in file_list :
            self.assertFalse("Le fichier test3.mkv devrait exister")    
        if not "test1_vostfr.mkv" in file_list :
            self.assertFalse("Le fichier test1_vostfr.mkv devrait exister")    
        if not "test2_vostfr.mkv" in file_list :
            self.assertFalse("Le fichier test2_vostfr.mkv devrait exister")
        if not "test3_vostfr.mkv" in file_list :
            self.assertFalse("Le fichier test3_vostr.mkv devrait exister")

        # TODO tester la liste des pistes du fichier


    def test_main_srt_only(self):
        """Teste la boucle entière du logiciel sur le dossier /data/srt contenant uniquement des fichiers .srt"""
        main.data_path = "/data/srt"
        main.is_dry_run = True

        main.main()

        file_list = os.listdir("/data/srt")

        print(f"filelist : {file_list}")
        
        self.assertEqual(len(file_list), 6, "Le dossier devrait comporter 6 fichiers")
        if not "ambigu.srt" in file_list :
            self.assertFalse("Le fichier ambigu.srt devrait exister")
        if not "familier.srt" in file_list :
            self.assertFalse("Le fichier familier.srt devrait exister")
        if not "soutenu.srt" in file_list :
            self.assertFalse("Le fichier soutenu.srt devrait exister")    
        if not "ambigu.fr.srt" in file_list :
            self.assertFalse("Le fichier ambigu.fr.srt devrait exister")    
        if not "familier.fr.srt" in file_list :
            self.assertFalse("Le fichier familier.fr.srt devrait exister")
        if not "soutenu.fr.srt" in file_list :
            self.assertFalse("Le fichier soutenu.fr.srt devrait exister")

        # TODO tester la liste des pistes du fichier

if __name__ == '__main__':
    unittest.main()




