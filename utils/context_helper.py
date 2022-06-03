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
            self.formats: dict = {}
            self.legals_path_file = self.root_path + "/data/context/legals.json"
            legals_file = open(self.legals_path_file)
            self.legals_sets = json.load(legals_file)
            # print(self.legals_sets)
            self.legals_map: dict = {
                self.legals_sets[k].get("name").lower(): k
                for k in self.legals_sets.keys()
            }
            # self.legals_map: dict = {}
            for format in self.config.get("formats"):
                try:
                    format_path_file: str = (
                        self.root_path + f"/data/context/{format}.json"
                    )
                    file = open(format_path_file)
                    format_dict = json.load(file)
                    file.close()
                    self.formats[format] = format_dict
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
        return self.config.get("basicLands") + [
            "snow-covered " + land for land in self.config.get("basicLands")
        ]

    def get_format_information(self, format: str) -> dict:
        return self.formats.get(format)

    def get_allowed_formats(self) -> list:
        return self.config.get("formats")

    def get_legal_sets(self) -> list:
        return self.legals_sets

    def get_legal_sets_names(self) -> list:
        legal_sets: list = self.legals_sets
        return [
            legal_sets[legal_set].get("name").strip().lower()
            for legal_set in legal_sets.keys()
        ]

    def add_new_legal_set(self, new_set: tuple) -> None:
        self.legals_sets[new_set["code"]] = {
            "name": new_set.get("name"),
            "release": new_set.get("release"),
        }
        legals_file = open(self.legals_path_file, "w+")
        json.dump(self.legals_sets, legals_file)
        legals_file.close()

    def get_set_info_by_code(self, set_code: str) -> dict:
        if set_code in self.legals_sets.keys():
            return self.legals_sets.get(set_code)
        else:
            return {}

    def get_set_info_by_name(self, set_name: str) -> dict:
        set_code: str = self.legals_map[set_name]
        output: dict = {"code": set_code}
        output.update(self.legals_sets[set_code])
        return output
