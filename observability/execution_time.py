import datetime
import logging
from logging import FileHandler, Formatter

logger = logging.getLogger("observability.execution_time")
logger.level = logging.INFO
handler = FileHandler("observability.log")
handler.setFormatter(Formatter("%(asctime)s %(message)s"))
logger.addHandler(handler)


def check_execution_time(method):
    """
    Decorator used to check how much time tooks the execution from a function
    """

    def decorator(*args, **kwargs):
        global logger
        start: datetime.datetime = datetime.datetime.now()
        method_name: str = str(method).split(" ")[1]
        output = method(*args, **kwargs)
        end: str = str(datetime.datetime.now() - start)
        log: str = f"{method_name} {end}"
        logger.info(log)
        return output

    return decorator
