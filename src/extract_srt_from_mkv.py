import os
from pathlib import Path
import subprocess

def extract_subtitle(mkv_file_str, output_file_str=None):
    # Gestion du fichier source
    if not os.path.isfile(mkv_file_str):
        raise FileNotFoundError(f"MKV file not found: {mkv_file_str}")
    
    if os.path.splitext(mkv_file_str)[1].lower() != ".mkv":
        raise ValueError(f"File {mkv_file_str} not supported")

    # Gestion du nom du fichier de sortie
    if output_file_str is None:
        base = os.path.splitext(mkv_file_str)[0]
        output_file_str = f"{base}.srt"

    # Obtenir la liste des pistes
    print(f"Analyse de {mkv_file_str}")
    try:
        result = subprocess.run(
            ["mkvmerge", "-i", mkv_file_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erreur lors de l'execution de mkvmerge -i : {e}")
   
    print(f"Info : {result.stdout}")

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
        raise ValueError(f"No subtitles tracks found in file : {mkv_file_str}")

    print(f"Extraction piste {subtitle_track_id} -> {output_file_str}")
    subprocess.run([
        "mkvextract", "tracks",
        mkv_file_str,
        f"{subtitle_track_id}:{output_file_str}"
    ])