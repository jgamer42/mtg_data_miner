#!/bin/bash
cd /Users/jaime/Mtg_proyect
source env/bin/activate
cd extract 
TDY=$(date +%F) 
scrapy crawl goldfish_staples -O salida.csv
cat salida.csv > ../data/goldfish_staples_${TDY}.csv
rm salida.csv         
deactivate
cd /Users/jaime