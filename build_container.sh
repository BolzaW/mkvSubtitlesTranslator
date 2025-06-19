#! /bin/bash
# Build le container et le sauvegarde sous la forme d'une archive
docker build -t mkv-subtitles-translator:latest .
docker save -o mkv-subtitles-translator.tar mkv-subtitles-translator:latest