cd .. 
source env/bin/activate
cd extract 
current_date=`date +%m-%d-%Y`
for format in "standard" "modern" "pioneer" "pauper"
do
    scrapy crawl goldfish_staples -a format=$format -O ../data/staples/goldfish_$format.csv
done