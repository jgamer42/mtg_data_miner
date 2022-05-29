import json
import pandas as pd
from io import TextIOWrapper


def export_data(file_to_export: str, data_to_export: dict, format="json") -> None:
    specific_export: function = eval(f"export_{format}")
    specific_export(file_to_export, data_to_export)


def export_json(path_to_export: str, data_to_export: dict) -> None:
    output_file: TextIOWrapper = open(path_to_export, "w+")
    json.dump(data_to_export, output_file)
    output_file.close()


def export_csv(path_to_export, data_to_export: dict):
    data = pd.DataFrame(data_to_export)
    data.to_csv(path_to_export)


def load_json(path_of_file: str) -> dict:
    file: TextIOWrapper = open(path_of_file, "r")
    raw_data = json.load(file)
    file.close()
    return raw_data
