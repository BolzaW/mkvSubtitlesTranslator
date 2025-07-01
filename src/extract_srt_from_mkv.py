import os
from pathlib import Path
import subprocess
import json

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
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", mkv_file_str],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erreur lors de l'execution de ffprobe : {e}")
   
    #print(f"Info : {result.stdout}")

    # Récupérer l'ID de la première piste de sous-titre
    # TODO gérer plusieurs pistes de sous titre

    tracks_json = json.loads(result.stdout)

    subtitle_track_id = -1
    for stream in tracks_json["streams"] :
        if stream["codec_type"] == "subtitle":
            subtitle_track_id = stream["index"]
            break
    
    if subtitle_track_id == -1:
        raise ValueError(f"No subtitles tracks found in file : {mkv_file_str}")

    
    print(f"Extraction piste {subtitle_track_id} -> {output_file_str}")
    try:
        subprocess.run([
            "ffmpeg", "-i", mkv_file_str, "-map", "0:s:0", "-an", "-vn", output_file_str]
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erreur lors de l'execution de ffmpeg -i : {e}")
