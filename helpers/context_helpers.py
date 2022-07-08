import os
import json
from operator import itemgetter


class Singelton(type):
    _instances: dict = {}
    """
    Class used as a singelton implementation
    this singelton implementation depends 
    of the format that is go to be loaded
    """

    def __call__(self, *args, **kwargs):
        format: str = kwargs.get("format", args[0])
        if format not in self._instances.keys():
            new_instance: Context = super().__call__(*args, **kwargs)
            self._instances[format] = new_instance
        return self._instances[format]


class Context(metaclass=Singelton):
    """
    Class used to handle the diferent formats
    and sets information
    """

    def __init__(self, format: str):
        file_path: str = os.path.dirname(__file__)
        context_path: str = f"{file_path}/context/{format}.json"
        if not os.path.exists(context_path):
            raise Exception("The format context Doesn't exists")
        data = open(context_path, "r")
        self.context_data: dict = json.loads(data.read())
        data.close()

    def get_older_format(self, list_of_formats: list) -> str:
        """
        Method to get the older format in a list
        :param list_of_formats: a list with the code formats to check Ie: ["VOW","MID","SNC"]
        :return str: the code of the older format Ie: "MID"
        """
        possible_formats: list = []
        for format in list_of_formats:
            possible_formats.append({"name": format, "date": list_of_formats})
        possible_formats.sort(key=itemgetter("released_at"))
        return possible_formats[0]["name"]
