#! /bin/bash
cd .. 
source env/bin/activate
cd extract 
current_date=`date +%m-%d-%Y`
cd API 
python mtg_api.py
cd ..
for format in "standard" "modern" "pioneer" "pauper"
do
    scrapy crawl mtg_wtf_formats -a format=$format -O ../data/context/$format.json
done
cd ..
deactivate