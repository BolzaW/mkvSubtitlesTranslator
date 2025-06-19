import os
import re
import pysrt
import deepl
from bs4 import BeautifulSoup
import time

def translate_srt_file(input_file, output_file, is_dry_run, keys_api_list=None, origin_lang="EN",target_lang="FR",
                        is_cleanup_subtitles=True, is_cleanup_songs=True):
    
    # Gestion de l'API Deepl
    valid_keys = []
    if not keys_api_list and not is_dry_run:
        raise ValueError("Pas de clés pour démarrer l'API DeepL")

    if keys_api_list and not is_dry_run:
        valid_keys = test_api_keys(keys_api_list)
        if not valid_keys :
            raise ValueError("Pas de clés valides pour démarrer l'API DeepL")
        
    # Lire le fichier avec pysrt
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"SRT file not found: {input_file}")
    subs = pysrt.open(input_file, encoding='utf-8')

    if is_cleanup_subtitles:
        subs = cleanup_subtitles(subs, is_cleanup_songs)

    if not is_dry_run:
        print(f"{count_chars_in_srt(subs)} caractères vont être envoyés à DeepL")

        #Convertit la liste des sous-titres en xml pour une traduction avec contexte par DeepL
        xml_subs = srt_to_xml(subs)
       
        key_index = 0
        tentative = 0
        is_translation_successful = False
        
        while (tentative < 3 and not is_translation_successful):

            # Call deepL API
            translator = deepl.Translator(valid_keys[key_index])

            try:     
                result = translator.translate_text(
                            xml_subs,
                            source_lang=origin_lang,
                            target_lang=target_lang,
                            model_type="prefer_quality_optimized",
                            tag_handling="xml",
                            context="Subtitles of a movie or TV show"
                        )
                
                xml_trads = result.text # type: ignore

                subs = xml_to_srt(xml_trads, subs)

                is_translation_successful = True

            except deepl.QuotaExceededException:
                print(f"❌ Quota DeepL dépassé")
                key_index += 1
                tentative += 1
                if key_index >= len(valid_keys):
                    print(f"❌ Plus de clés valides disponnibles, traduction impossible")
                    break
                
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
        print(f"{count_chars_in_srt(subs)} caractères auraient du être envoyés à DeepL (DRY RUN)")

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

        # Cas 5 - Nettoyage des espaces superflux :
        text = re.sub(r"  ", " ", text)

        # Cas 6 — Supprimer les lignes sans alphanumérique
        lines = text.splitlines()
        lines = [line for line in lines if re.search(r"[A-Za-z0-9]", line)]
        text = "\n".join(lines)

        # Cas 7 — Si tout le texte est encore vide ou sans alphanumérique
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

def srt_to_xml(subs):
    xml_to_translate = ""
    
    for sub in subs:
        # Nettoyer le texte pour une compatibilité XML basique
        clean_text = sub.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        xml_to_translate += f'<str id="{sub.index}">{clean_text}</str>\n'
    
    return xml_to_translate

def xml_to_srt(xml,subs):
    translated_text_list = []
    translated_subs = []
    soup = BeautifulSoup(xml, 'html.parser')
    for tag in soup.find_all('str'):
        translated_text_list.append(tag.get_text())
    
    for index, sub in enumerate(subs):
        sub.text = translated_text_list[index]
        translated_subs.append(sub)

    return pysrt.SubRipFile(items=translated_subs)

def count_chars_in_srt(subs):
    total_sent_chars = 0
    for sub in subs:
        total_sent_chars += len(sub.text)

    return total_sent_chars

    
