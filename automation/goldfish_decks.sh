#! /bin/bash
cd .. 
source env/bin/activate
cd extract 
current_date=`date +%m-%d-%Y`
for format in "standard" "modern" "pioneer" "pauper"
do
    scrapy crawl goldfish_decks -a format=$format -O ../data/$format.json
    cd ../transform
    python clean_decks.py --format=$format
    output_raw_file="${format}_${current_date}"
    mv ../data/$format.json ../data/raw/goldfish_decks_$output_raw_file.json
    cd ../extract
done
cd ..
deactivate