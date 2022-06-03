def clean_list(data: list) -> None:
    for element in data:
        try:
            if type(element) == dict:
                clean_dict(element)
            elif type(element) == list:
                clean_list(element)
            elif type(element) == str:
                element = element.replace("\n", "").strip()
                element = element.replace("\xa0", "").strip()
        except:
            continue


def clean_dict(data: dict) -> None:
    for key in data.keys():
        if type(data[key]) == dict:
            clean_dict(data[key])
        elif type(data[key]) == list:
            clean_list(data[key])
        elif type(data[key]) == str:
            data[key] = data[key].replace("\n", "").strip()
            data[key] = data[key].replace("\xa0", "").strip()


def dict_list_2_list(data: dict) -> list:
    output: list = []
    for key in data:
        output += data[key]
    return output


def normalize_string(string_to_clean: str) -> str:
    return string_to_clean.strip().lower()
