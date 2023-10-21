import json
import os


# get_mode_info - функция, возвращающая словарь из Data/modes.json.
def get_mode_info():
    path = os.path.abspath(os.curdir)
    try:
        with open(path + '\\Data\\modes.json', mode='r', encoding='utf-8') as file:
            info = json.load(file)
    except Exception as e:
        info = {'study': {},
                'answer': {}}
    return info


# dump_mode_info - функция, загружающая словарь info в Data/modes.json.
def dump_mode_info(info):
    path = os.path.abspath(os.curdir)
    with open(path + '\\Data\\modes.json', mode='w', encoding='utf-8') as file:
        json.dump(info, file, ensure_ascii=False)
