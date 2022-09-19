import copy
import re


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


def normalize_dict(dict_to_normalize: dict) -> dict:
    output: dict = copy.deepcopy(dict_to_normalize)
    for element in output.keys():
        if type(output[element]) == str:
            output[element] = normalize_str(output[element])
        if type(output[element]) == float:
            output[element] = float("{:.3f}".format(output[element]))
        if type(output[element]) == dict:
            output[element] = normalize_dict(output[element])
    return output
