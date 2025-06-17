import os
import random
import re
import pysrt
import deepl
import time


def translate_srt_file(input_file, output_file, is_dry_run, origin_lang="EN",target_lang="FR",
                        keys_api_list=None, is_cleanup_subtitles=True, is_cleanup_songs=True):
    
    # Gestion de l'API Deepl
    valid_keys = []
    if not keys_api_list and not is_dry_run:
        raise ValueError("Pas de clés pour démarrer l'API DeepL")

    if keys_api_list and not is_dry_run:
        valid_keys = test_api_keys(keys_api_list)
        if not valid_keys :
            raise ValueError("Pas de clés valides pour démarrer l'API DeepL")
        
    # 🔍 Lire le fichier avec pysrt
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"SRT file not found: {input_file}")
    subs = pysrt.open(input_file, encoding='utf-8')

    if is_cleanup_subtitles:
        subs = cleanup_subtitles(subs, is_cleanup_songs)

    
    total_sent_chars = 0
    list_subs_text = []
    for sub in subs:
        total_sent_chars += len(sub.text)
        list_subs_text.append(sub.text)
        
    if not is_dry_run:
        print(f"{total_sent_chars} caractères vont être envoyés à DeepL")
       
        key_index = 0
        tentative = 0
        is_translation_successful = False
        
        while (tentative < 3 and not is_translation_successful):

            # Call deepL API
            translator = deepl.Translator(valid_keys[key_index])

            try:     
                result = translator.translate_text(
                            list_subs_text,
                            source_lang=origin_lang,
                            target_lang=target_lang
                        )
                is_translation_successful = True
            
            except deepl.QuotaExceededException:
                print(f"❌ Quota DeepL dépassé")
                key_index += 1
                tentative += 1
                
            except deepl.TooManyRequestsException:
                tentative += 1
                print(f"❌ DeepL surchargé. Essai {tentative}/3. Retry dans 1s")
                time.sleep(1)
            
            except deepl.DeepLException as e:
                tentative += 1
                print(f"❌ Erreur DeepL innatendue : {e}. Essai {tentative}/3. Retry dans 1s")

        if not is_translation_successful:
            raise RuntimeError("La traduction DeepL a échoué")
    else:
        print(f"{total_sent_chars} caractères auraient du être envoyés à DeepL (DRY RUN)")

    # 💾 Sauvegarder
    subs.save(output_file, encoding='utf-8')
    print(f"✅ Fichier traduit sauvegardé : {output_file}")

def cleanup_subtitles(subs, clean_music=True):
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

def test_api_keys(key_list):
    valid_keys = []
    
    for key in  key_list:
        try:
            translator = deepl.Translator(key)
            translator.translate_text(
                    text="Hi",
                    source_lang="EN",
                    target_lang="FR"
                )
            valid_keys.append(key)
        except deepl.DeepLException as e:
            print(f"Clé DeepL {key} invalide! {e}")
    
    return valid_keys

    
