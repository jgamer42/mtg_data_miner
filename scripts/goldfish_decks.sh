#!/bin/bash
cd /Users/jaime/Mtg_proyect
source env/bin/activate
cd extract 
TDY=$(date +%F) 
scrapy crawl goldfish_decks -O salida.csv
cat salida.csv > ../data/goldfish_decks_${TDY}.json
rm salida.csv         
deactivate
cd /Users/jaime