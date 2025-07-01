#!/bin/bash
docker load -i mkv-subtitles-translator.tar
docker-compose up
docker-compose down
docker image rm mkv-subtitles-translator