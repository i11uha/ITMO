import time
from copy import deepcopy

from Main import toml_lines_to_bytes
from dop1 import toml_lines_to_json_bytes
from dop2 import toml_lines_to_json
from dop3 import toml_lines_to_xml_bytes

def check_speed(input_data, func):
    start = time.time()
    for _ in range(100):
        data = deepcopy(input_data)
        func(data)
    return time.time() - start

with open("input.toml", "r", encoding="utf-8") as f:
    toml_lines = f.readlines()

t1 = check_speed(toml_lines, toml_lines_to_bytes)
t2 = check_speed(toml_lines, toml_lines_to_json_bytes)
t3 = check_speed(toml_lines, toml_lines_to_json)
t4 = check_speed(toml_lines, toml_lines_to_xml_bytes)

print(f"Обязательное задание     : {t1:.4f} с")
print(f"Доп. задание №1 (JSON)   : {t2:.4f} с")
print(f"Доп. задание №2 (JSON)    : {t3:.4f} с")
print(f"Доп. задание №3 (XML)    : {t4:.4f} с")