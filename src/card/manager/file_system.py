import json
import os

from dotenv import load_dotenv

load_dotenv()


class FileSystem:
    def __init__(self, card: object):
        self.card: object = card
        self.types_to_export: list = [list, dict, str, int]
        self.exclude_fields: list = [
            "raw_data",
            "clean_attributes",
            "managers",
            "prices",
        ]
        card_name = str(card)
        if "//" in str(card) or "/" in str(card):
            card_name = str(card).replace("/", "").strip()
        self.path: str = (
            os.getenv("MTG_PROJECT_ROOT_PATH", "") + f"/data/cards/{card_name}.json"
        )
        self.clean_data: dict = {}
        raw_data: dict = vars(self.card)
        for k in raw_data:
            if (
                k not in self.exclude_fields
                and type(raw_data[k]) in self.types_to_export
            ):
                self.clean_data[k] = raw_data[k]

    def export(self, format: str):
        handler = getattr(self, f"export_{format}")
        handler()

    def export_json(self):
        output_file = open(self.path, "w")
        json.dump(self.clean_data, output_file)
        output_file.close()

    def find(self) -> bool:
        return os.path.exists(self.path)

    def load(self) -> dict:
        input_file = open(self.path, "r")
        data: dict = json.load(input_file)
        input_file.close()
        return data
