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
        return self.config.get("formats_meta_info").get(format)
