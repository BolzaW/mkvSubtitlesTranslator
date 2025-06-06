import argparse
import os
import sys
import tempfile

# Import des fonctions depuis les scripts existants
import extract_srt_from_mkv
import translate_srt
import merge_srt_in_mkv

def main():

    # --- Argument CLI ---
    parser = argparse.ArgumentParser(description="Traduction de fichiers .srt via DeepL")
    parser.add_argument("input_file", help="Chemin vers le fichier MKV d'entrée")
    parser.add_argument("output_file", default=None, help="Chemin vers le fichier MKV de sortie")
    parser.add_argument("--dry-run", action="store_true", help="Nettoie le SRT sans le traduire (aucune requête DeepL)")
    parser.add_argument("--lang", default="FR", help="Langue de traduction (ex: FR, EN, DE, etc.)")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    is_dry_run = args.dry_run
    target_lang = args.lang.upper()

    if not os.path.isfile(input_file):
        print(f"Fichier MKV introuvable : {input_file}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        extracted_srt = os.path.join(tmpdir, "original.srt")
        translated_srt = os.path.join(tmpdir, "translated.srt")

        print("📤 Étape 1 : Extraction des sous-titres...")
        extract_srt_from_mkv.extract_subtitle(input_file, extracted_srt)

        print("🌐 Étape 2 : Traduction avec DeepL..." + (" (simulation)" if is_dry_run else ""))
        translate_srt.translate_srt_file(
            input_file=extracted_srt,
            output_file=translated_srt,
            target_lang=target_lang,
            is_dry_run=is_dry_run
        )

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







