import subprocess
import os

def add_subtitle_to_mkv(mkv_file, srt_file, output_file=None, language='FR', track_name='French Subs'):
    if not os.path.isfile(mkv_file):
        raise FileNotFoundError(f"MKV file not found: {mkv_file}")
    if not os.path.isfile(srt_file):
        raise FileNotFoundError(f"SRT file not found: {srt_file}")

    if output_file is None:
        base, ext = os.path.splitext(mkv_file)
        output_file = f"{base}_vostfr{ext}"
   
    command = [
        "ffmpeg",
        "-i", mkv_file,
        "-i", srt_file,
        "-map", "0",
        "-map", "1:0",
        "-c", "copy", 
        "-c:s", "srt",
        # TODO Add metadata -> besoin de connaitre le nouvel index de la piste de sous-titre
        # "-metadata:s:s:?", "language=FR",
        # "-metadata:s:s:?", "title=Français (traduit)",
        output_file
    ]

    print("Running command:", " ".join(command))
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erreur lors de l'execution de ffmpeg : {e}")
    print(f"Subtitles added successfully to: {output_file}")
