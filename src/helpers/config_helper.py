import os
import json
import argparse


class configHelper(object):
    """
    Object used to read the config.json with the config of the project
    this object use a singelton implementation
    """

    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(configHelper, self).__new__(self)
            self.root_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
            path_to_config_file = self.root_path + "/config.json"
            file = open(path_to_config_file, "r")
            self.config = json.load(file)
            self.dataset_path = self.config.get("DatasetPath")
            file.close()
        return self.instance

    def args_constraint(self, config: dict = {}) -> dict:
        """
        Method used to add args config to a script
        :param config: A dict with the config with additional params
        :return dict: A dict with the params inserted
        """
        parser = argparse.ArgumentParser()
        for conf in self.config.get("DefaultParams", []):
            parser.add_argument(
                f"--{conf.get('name')}",
                required=bool(conf.get("required", False)),
                help=conf.get("help", "not help configured fot this param"),
            )
        if config:
            for conf in config.keys():
                parser.add_argument(
                    f"--{conf}",
                    required=config[conf].get("required", False),
                    help=config[conf].get("help", ""),
                )
        return vars(parser.parse_args())

    def get_dataset_path(self) -> str:
        """
        Function used to get the folder to store the data
        :return str: Str with the path to store the information
        """
        return f"{self.root_path}/{self.dataset_path}"

    def get_clean_decks_path(self) -> str:
        """
        Function used to get the folder to store the clean decks
        :return str: Str with the path to store the information
        """
        return f"{self.root_path}/{self.dataset_path}/clean/decks"
