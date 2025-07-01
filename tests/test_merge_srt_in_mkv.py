import unittest
import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from merge_srt_in_mkv import add_subtitle_to_mkv

class TestMergeSubtitles(unittest.TestCase):
    mkv_test_file_path = "/app/test_data/mkv_to_srt/test.mkv"
    srt_file_path = "/app/test_data/mkv_to_srt/expected.srt"
    output_mkv = "/app/test_data/mkv_to_srt/test_vostfr.mkv"
    output_defined = "/app/test_data/mkv_to_srt/test_defined_output.mkv"

    def tearDown(self):
        if os.path.exists(self.output_mkv):
            os.remove(self.output_mkv)
        if os.path.exists(self.output_defined):
            os.remove(self.output_defined)
    
    def test_merge_1srt_in_1mkv(self):
        """Teste la fonction de merge (nominal)"""
        add_subtitle_to_mkv(self.mkv_test_file_path, self.srt_file_path)
        self.assertTrue(os.path.isfile(self.output_mkv), "Le fichier test.mkv devrait exister")

        result = subprocess.run(
            ["ffprobe", "-hide_banner", str(self.output_mkv)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        
        tracks = [ 
            track for track in result.stderr.splitlines()
            if "stream" in track.lower()
        ]

        print(f"tracks = {tracks}")
       
        self.assertEqual(len(tracks), 5, "La video devrait comporter 5 pistes")

        self.assertTrue("Video: msmpeg4v3" in tracks[0], "Le mkv devrait avoir une piste vidéo")
        self.assertTrue("Audio: vorbis" in tracks[1], "Le mkv devrait avoir une piste audio")
        self.assertTrue("Subtitle: subrip" in tracks[2], "Le mkv devrait avoir une piste sous-titre")
        self.assertTrue("Subtitle: subrip" in tracks[3], "Le mkv devrait avoir une piste sous-titre")
        self.assertTrue("Subtitle: subrip" in tracks[4], "Le mkv devrait avoir une piste sous-titre")

    def test_merge_with_output_defined(self):
        """Teste la fonction de merge avec un fichier output sépcifié"""
        add_subtitle_to_mkv(self.mkv_test_file_path, self.srt_file_path, self.output_defined)

        self.assertTrue(os.path.isfile(self.output_defined), "Le fichier test.mkv devrait exister")

        result = subprocess.run(
            ["ffprobe", "-hide_banner", str(self.output_defined)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
        tracks = [ 
            track for track in result.stderr.splitlines()
            if "stream" in track.lower()
        ]
        print(f"tracks = {tracks}")
       
        self.assertEqual(len(tracks), 5, "La video devrait comporter 5 pistes")

        self.assertTrue("Video: msmpeg4v3" in tracks[0], "Le mkv devrait avoir une piste vidéo")
        self.assertTrue("Audio: vorbis" in tracks[1], "Le mkv devrait avoir une piste audio")
        self.assertTrue("Subtitle: subrip" in tracks[2], "Le mkv devrait avoir une piste sous-titre")
        self.assertTrue("Subtitle: subrip" in tracks[3], "Le mkv devrait avoir une piste sous-titre")
        self.assertTrue("Subtitle: subrip" in tracks[4], "Le mkv devrait avoir une piste sous-titre")

    def test_merge_not_found_srt(self):
        """Teste la fonction de merge avec un fichier srt introuvable"""
        with self.assertRaises(FileNotFoundError):
            add_subtitle_to_mkv(self.mkv_test_file_path, "/app/test_data/mkv_to_srt/unknown.srt")

    def test_merge_not_found_mkv(self):
        """Teste la fonction de merge avec un fichier mkv introuvable"""
        with self.assertRaises(FileNotFoundError):
            add_subtitle_to_mkv("/app/test_data/mkv_to_srt/unknown.mkv", self.srt_file_path)

    def test_merge_bad_srt(self):
        """Teste la fonction de merge avec un fichier srt incorrect"""
        with self.assertRaises(RuntimeError):
            add_subtitle_to_mkv(self.mkv_test_file_path, "/app/test_data/mkv_to_srt/bad.srt")

    def test_merge_bad_mkv(self):
        """Teste la fonction de merge avec un fichier mkv incorrect"""
        with self.assertRaises(RuntimeError):
            add_subtitle_to_mkv("/app/test_data/mkv_to_srt/bad.mkv", self.srt_file_path)
        

if __name__ == '__main__':
    unittest.main()





