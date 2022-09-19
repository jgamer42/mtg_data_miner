import logging
from src.format.format_controller import Format
from src.deck.deck_controller import Deck
from src.card.card_controller import Card
from src.card.manager.file_system import FileSystem
import pandas as pd

logging.getLogger("scrapy").propagate = False
logging.getLogger("filelock").propagate = False
logging.getLogger("urllib3.connectionpool").propagate = False
logging.getLogger("telethon.extensions.messagepacker").propagate = False
logging.getLogger("telethon.network.mtprotosender").propagate = False
a = Format("standard")
a.get_spiders_data()
a.build_report()
a.export()
data = pd.DataFrame(a.processed_data)
data.to_csv("legacy.csv")
