import os
from pathlib import Path
import subprocess

def extract_subtitle(mkv_file_str, output_file_str=None):
    if not os.path.isfile(mkv_file_str):
        raise FileNotFoundError(f"MKV file not found: {mkv_file_str}")
    mkv_file = Path(mkv_file_str)

    if output_file_str is None:
        base, ext = os.path.splitext(mkv_file)
        output_file_str = f"{base}_vostfr{ext}"
        output_file = Path(output_file_str)
    else :
        output_file = Path(output_file_str)

    # Obtenir la liste des pistes
    print(f"🔍 Analyse de {mkv_file.name}")
    result = subprocess.run(
        ["mkvmerge", "-i", str(mkv_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"Info : {result}")

    # Récupérer l'ID de la première piste de sous-titre
    # TODO gérer plusieurs pistes de sous titre
    subtitle_track_id = -1
    for line in result.stdout.splitlines():
        if "subtitles" in line.lower():
            parts = line.split(':', 1)
            if len(parts) >= 2:
                track_id = parts[0].split()[2]
                subtitle_track_id = int(track_id)
                break

    if subtitle_track_id == -1:
        print(f"⚠️  Aucun sous-titre trouvé dans {mkv_file.name}")
        return

    print(f"📤 Extraction piste {subtitle_track_id} -> {output_file.name}")
    subprocess.run([
        "mkvextract", "tracks",
        str(mkv_file),
        f"{subtitle_track_id}:{str(output_file)}"
    ])

#Test
if __name__ == "__main__":
    mkv_file_str = "/app/samples/mkv/test.mkv"
    output_file_str = "/app/samples/srt/test.srt"
    extract_subtitle(mkv_file_str, output_file_str)