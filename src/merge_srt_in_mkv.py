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
        "mkvmerge",
        "-o", output_file,
        mkv_file,
        "--language", f"0:{language}",
        "--track-name", f"0:{track_name}",
        srt_file
    ]

    print("Running command:", " ".join(command))
    subprocess.run(command, check=True)
    print(f"Subtitles added successfully to: {output_file}")
