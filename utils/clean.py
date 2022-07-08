import re
import copy
from typing import Union


def clean_list(data: list) -> list:
    raw_data: list = copy.deepcopy(data)
    cleaned_data: list = []
    aux: Union[str, list, dict] = []
    for element in raw_data:
        if type(element) == dict:
            aux = clean_dict(element)
        elif type(element) == list:
            aux = clean_list(element)
        elif type(element) == str:
            aux = element.replace("\n", "").replace("\xa0", "").strip()
        cleaned_data.append(aux)
    return cleaned_data


def clean_dict(data: dict) -> dict:
    output: dict = copy.deepcopy(data)
    for key in output.keys():
        if type(output[key]) == dict:
            output[key] = clean_dict(output[key])
        elif type(output[key]) == list:
            output[key] = clean_list(output[key])
        elif type(output[key]) == str:
            output[key] = output[key].replace("\n", "").replace("\xa0", "").strip()
    return output


def dict_list_2_list(data: dict) -> list:
    output: list = []
    for key in data:
        output += data[key]
    return output


def normalize_str(string_to_clean: str) -> str:
    return string_to_clean.strip().lower()


def clean_str(string_to_clean: str) -> str:
    noise = re.findall(r"[\(\d\)]|\+| MDFCs", string_to_clean)
    aux = string_to_clean
    for n in noise:
        aux = aux.replace(n, "")
    return normalize_str(aux)
