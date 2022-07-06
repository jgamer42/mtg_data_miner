import logging
from src.format.controller import Format
logging.getLogger("scrapy").propagate=False
logging.getLogger("filelock").propagate=False
a = Format("pioneer")
a.get_spiders_data()
