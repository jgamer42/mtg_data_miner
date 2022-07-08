import logging
from src.format.format_controller import Format

logging.getLogger("scrapy").propagate = False
logging.getLogger("filelock").propagate = False
logging.getLogger("urllib3.connectionpool").propagate = False
a = Format("pioneer")
a.get_spiders_data()
