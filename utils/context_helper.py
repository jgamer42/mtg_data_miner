import os
import json


class contextHelper(object):
    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(contextHelper, self).__new__(self)
            self.root_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
            path_to_config_file = self.root_path + "/context.json"
            file = open(path_to_config_file)
            self.config = json.load(file)
            file.close()
            self.legals_path_file = self.root_path + "/data/context/legals.json"
            legals_file = open(self.legals_path_file)
            self.legals_sets = json.load(legals_file)
            self.formats: dict = {}
            for format in self.config.get("formats"):
                try:
                    format_path_file: str = (
                        self.root_path + f"/data/context/{format}.json"
                    )
                    file = open(format_path_file)
                    format_dict = json.load(file)
                    self.formats[format] = format_dict[0]
                except FileNotFoundError:
                    continue

        return self.instance

    def get_noise_type_sets(self) -> list:
        return self.config.get("noiseTypeSets")

    def get_noise_codes(self) -> list:
        return self.config.get("noiseCodes")

    def get_posible_card_sections(self) -> list:
        return self.config.get("cardMainTypes")

    def get_basic_lands(self) -> list:
        return self.config.get("basicLands")

    def get_format_information(self, format: str) -> dict:
        return self.formats.get(format)

    def get_allowed_formats(self) -> list:
        return self.config.get("formats")

    def get_legal_sets(self) -> list:
        return self.legals_sets

    def add_new_legal_set(self, new_set: tuple) -> None:
        self.legals_sets[new_set[0]] = new_set[1]
        legals_file = open(self.legals_path_file, "w+")
        json.dump(self.legals_sets, legals_file)
        legals_file.close()
