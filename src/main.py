import os
import sys
import tempfile
import shutil

# Import des fonctions depuis les scripts existants
import extract_srt_from_mkv
import translate_srt
import merge_srt_in_mkv

data_path = "/data"

def main():
    # Gestion des variables d'environnement
    overwrite_files = os.getenv("OVERWRITE_FILES", "false").lower() == "true"
    keep_srt_files = os.getenv("KEEP_SRT_FILES", "false").lower() == "true"
    cleanup_subtitles = os.getenv("CLEANUP_SUBTITLES", "true").lower() == "true"
    cleanup_songs = os.getenv("CLEANUP_SONGS_SUBTITLES", "true").lower() == "true"
    is_dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    origin_lang = os.getenv("ORIGIN_LANG", "EN").upper()
    target_lang = os.getenv("TARGET_LANG", "FR").upper()
    list_api_keys = [key.strip() for key in os.getenv("OVERWRITE_FILES", "default").split(",") if key.strip()]

    # Création de la liste de fichiers mkv à traduire
    list_mkv_files = [
        file for file in os.listdir(data_path) 
        if file.lower().endswith(".mkv") and os.path.isfile(os.path.join(data_path, file))
    ]
    if not list_mkv_files:
        print(f"Aucun fichier .mkv dans le dossier {data_path}. FIN")
        sys.exit(1)
    else:
        print(f"{len(list_mkv_files)} fichiers .mkv à traiter dans {data_path}")
        for file in list_mkv_files:
            print(f" - {file}")

    count = 0
    for file in list_mkv_files:
        count += 1
        input_file = os.path.join(data_path, file)
        output_file = os.path.join(data_path, os.path.splitext(file)[0] + "_vostfr.mkv")
        print(f"Traduction des sous-titres du fichier {input_file} {count}/{len(list_mkv_files)}")
               
        with tempfile.TemporaryDirectory() as tmpdir:
            extracted_srt = os.path.join(tmpdir, "extracted.srt")
            translated_srt = os.path.join(tmpdir, "translated.srt")

            print("📤 Étape 1 : Extraction des sous-titres...")
            extract_srt_from_mkv.extract_subtitle(input_file, extracted_srt)
            if keep_srt_files:
                shutil.copy2(extracted_srt,os.path.join(data_path, os.path.splitext(file)[0] + ".srt"))


            print("🌐 Étape 2 : Traduction avec DeepL..." + (" (simulation)" if is_dry_run else ""))
            translate_srt.translate_srt_file(
                input_file=extracted_srt,
                output_file=translated_srt,
                target_lang=target_lang,
                is_dry_run=is_dry_run
            )
            if keep_srt_files:
                shutil.copy2(translated_srt,os.path.join(data_path, os.path.splitext(file)[0] + ".fr.srt"))

            print("📥 Étape 3 : Injection du fichier SRT traduit dans le MKV...")
            merge_srt_in_mkv.add_subtitle_to_mkv(
                mkv_file=input_file,
                srt_file=translated_srt,
                output_file=output_file,
                language=target_lang.lower(),
                track_name=f"{target_lang} Subs"
            )

            print("✅ Terminé ! Fichier final :", output_file)

if __name__ == "__main__":
    main()







