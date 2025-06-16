import os
from pathlib import Path
import subprocess

def extract_subtitle(mkv_file_str, output_file_str=None):
    # Gestion du fichier source
    if not os.path.isfile(mkv_file_str):
        raise FileNotFoundError(f"MKV file not found: {mkv_file_str}")
    
    if os.path.splitext(mkv_file_str)[1].lower() != ".mkv":
        raise ValueError(f"File {mkv_file_str} not supported")
    
    mkv_file = Path(mkv_file_str)

    # Gestion du nom du fichier de sortie
    if output_file_str is None:
        base = os.path.splitext(mkv_file)[0]
        output_file_str = f"{base}.srt"
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
    if result.returncode != 0:
        raise RuntimeError(f"Erreur lors de l'exécution de mkvmerge (code {result.returncode}):\n{result.stderr.strip()}") 
    
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

    print(f"📤 Extraction piste {subtitle_track_id} -> {output_file.name}")
    subprocess.run([
        "mkvextract", "tracks",
        str(mkv_file),
        f"{subtitle_track_id}:{str(output_file)}"
    ])