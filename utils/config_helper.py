import os
import json
import argparse


class configHelper(object):
    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(configHelper, self).__new__(self)
            self.root_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
            path_to_config_file = self.root_path + "/config.json"
            file = open(path_to_config_file)
            self.config = json.load(file)
            file.close()
        return self.instance

    def args_constraint(self, config: dict = {}):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--format",
            required=True,
            help="The format to clean",
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
        return f"{self.root_path}/{self.config.get('DatasetPath')}"

    def get_datamarket_path(self) -> str:
        return f"{self.root_path}/{self.config.get('DataMarketPath')}"

    def get_context_path(self) -> str:
        return f"{self.root_path}/{self.config.get('ContextPath')}"

    def get_mtg_api_card(self) -> str:
        return self.config.get("mtgApi_card")

    def get_clean_decks_path(self) -> str:
        return self.get_datamarket_path() + "/decks/"
