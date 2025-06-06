import argparse
import os
import re
import pysrt
import deepl
import time

# 🗝️ Clé API DeepL
DEEPL_API_KEY = ""
translator = deepl.Translator(DEEPL_API_KEY)

def translate_srt_file(input_file, output_file, is_dry_run, target_lang="FR"):

    # 🔍 Lire le fichier avec pysrt
    if not os.path.isfile(input_file):
            raise FileNotFoundError(f"SRT file not found: {input_file}")
    subs = pysrt.open(input_file, encoding='utf-8')

    subs = cleanup_subtitle(subs)

    total_sent_chars = 0

    if not is_dry_run:

        stop_translation = False
        count = 0
        
        for sub in subs:
            max_retries = 3
            attempts = 0

            # Traduction avec retry en cas d'erreur
            while attempts < max_retries:
                try:
                    #print(f"Traduction de '{sub.text}' en cours ...")
                    count += 1
                    total_sent_chars += len(sub.text) # type: ignore

                    result = translator.translate_text(
                        sub.text, # type: ignore
                        source_lang="EN",
                        target_lang=target_lang
                    )
                    sub.text = result
                    attempts = 0
                    # print(f"Traduction de '{sub.text}' en '{result.text}'")
                    print(f"\rTraduction: {count}/{len(subs)}  Nombre de caractères envoyés: {total_sent_chars}", end="", flush=True)
                    break

                except deepl.QuotaExceededException:
                    print()
                    print("❌ Quota DeepL dépassé.")
                    stop_translation = True
                    break
                except deepl.TooManyRequestsException:
                    attempts += 1
                    count -= 1
                    print()
                    print(f"❌ DeepL surchargé. Essai {attempts}/{max_retries}. Retry dans 1s")
                    time.sleep(1)
                except Exception as e:
                    print()
                    print(f"⚠️ Erreur lors de la traduction : {e}")
                    stop_translation = True
                    break

            if stop_translation:
                break
        print()
        print(f"🔢 Total de caractères envoyés à DeepL : {total_sent_chars}")

    else:
        for sub in subs:
            total_sent_chars += len(sub.text) 
            
        print(f"🔢 Total de caractères du fichier srt : {total_sent_chars}")

    # 💾 Sauvegarder
    subs.save(output_file, encoding='utf-8')
    print(f"✅ Fichier traduit sauvegardé : {output_file}")

def cleanup_subtitle(subs, clean_music=True):
# Nettoyage des sous-titres : suppression ou simplification
    cleaned_subs = []
    for sub in subs:
        text = sub.text.strip()

         # Cas 1 — Sous-titre uniquement [xxx]
        if re.fullmatch(r"\[\s*[^]]+\s*\]", text, re.IGNORECASE):
            continue

        # Cas 2 — Supprimer [ ... ]
        text = re.sub(r"\[\s*[^]]+\s*\]", "", text)

        if clean_music:
            # Cas 3 — Supprimer ♪...♪
            text = re.sub(r"♪♪.*?♪♪", "", text)
            text = re.sub(r"♪♪.*?♪", "", text)
            text = re.sub(r"♪.*?♪♪", "", text)
            text = re.sub(r"♪.{1,}?♪", "", text)

            # Cas 4 — Supprimer ♪...♪ sur plusieurs lignes
            text = re.sub(r"♪♪.{3,}?♪♪", "", text, flags=re.DOTALL)
            text = re.sub(r"♪♪.{3,}?♪", "", text, flags=re.DOTALL)
            text = re.sub(r"♪.{3,}?♪♪", "", text, flags=re.DOTALL)
            text = re.sub(r"♪.{3,}?♪", "", text, flags=re.DOTALL)


        # Cas 5 — Supprimer les lignes sans alphanumérique
        lines = text.splitlines()
        lines = [line for line in lines if re.search(r"[A-Za-z0-9]", line)]
        text = "\n".join(lines)

        # Cas 6 — Si tout le texte est encore vide ou sans alphanumérique
        if not re.search(r"[A-Za-z0-9]", text):
            continue

        # Nettoyage final
        text = text.strip()
        if not text:
            continue  # ignore les sous-titres vides après nettoyage

        sub.text = text
        cleaned_subs.append(sub)

    return pysrt.SubRipFile(items=cleaned_subs)

# test
if __name__ == "__main__":

    input_file = "/app/samples/srt/test.srt"
    output_file = "/app/samples/srt_fr/test.srt"
    is_dry_run = True
    translate_srt_file(input_file, output_file, is_dry_run)