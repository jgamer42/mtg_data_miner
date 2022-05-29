# Aditional info

- For get deep card info is used this [API](https://docs.magicthegathering.io/)

- For get the price of the cards is used the page [TCGPlayer](https://shop.tcgplayer.com/magic?newSearch=true) because starcitygames blocks the scraping

- For metagame info is used:  
  - Scrapped the page [MtgGoldfish](https://www.mtggoldfish.com/metagame/standard#paper)
  - Use the [mtgMeta](https://mtgmeta.io/docs)

## Tecnologies

- scrapy
- pandas
- mypy
- Apache airflow

## Flows enabled

- Traditional magic formats

## Main questions

- What is the cheapest format on Magic
- Which de dominant collection on each format
- Who is the strongest color on each format

## To do

- Migrate the scrappy section to MyPy
- Documentate all system and use pydoc to generate the doc
- Automate the formats rotation
- Build the flow to commander format
- Check the dupply code when reading args in the scripts

## Doc

- The data folder is used to store the raw decks mined

## Tools

- Run the MTG_API to download the noised and Legals sets
- Run the mtg_wtk spider to update the collections sets
