# Author = Safin Ilya Dmitrievich
# Group = P3106
# Date = 18.11.2025

import sys
from Main import TOMLParser


def _escape_string(s: str) -> str:
    # экранирование
    escape_dict = {
        '"': '\\"',
        '\\': '\\\\',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\b': '\\b',
        '\f': '\\f'
    }
    return ''.join(escape_dict.get(c, c) for c in s)


def _to_pretty_json_worker(obj, indent_level: int = 0) -> str:
    indent_step = "  "  # 2 пробела на шаг отступа
    current_indent = indent_step * indent_level
    next_indent = indent_step * (indent_level + 1)

    if obj is None:
        return 'null'
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, (int, float)):
        if isinstance(obj, float):
            s = str(obj)
            if s in ('inf', '-inf', 'nan'):
                raise ValueError(f"Float value {obj} is not JSON serializable")
        return str(obj)
    elif isinstance(obj, str):
        return '"' + _escape_string(obj) + '"'
    elif isinstance(obj, list):
        if not obj:
            return '[]'
        items = []
        for item in obj:
            val_str = _to_pretty_json_worker(item, indent_level + 1)
            items.append(next_indent + val_str)

        inner = ',\n'.join(items)
        return '[\n' + inner + '\n' + current_indent + ']'
    elif isinstance(obj, dict):
        if not obj:
            return '{}'
        pairs = []
        for key, value in obj.items():
            if not isinstance(key, str):
                key = str(key)
            key_json = '"' + _escape_string(key) + '"'
            value_json = _to_pretty_json_worker(value, indent_level + 1)
            pairs.append(next_indent + key_json + ': ' + value_json)

        inner = ',\n'.join(pairs)
        return '{\n' + inner + '\n' + current_indent + '}'
    else:
        return '"' + _escape_string(str(obj)) + '"'


def python_obj_to_pretty_json_bytes(obj) -> bytes:
    json_str = _to_pretty_json_worker(obj, indent_level=0)
    return (json_str + '\n').encode('utf-8')


def main():
    try:

        parser = TOMLParser()

        with open("input.toml", "r", encoding="utf-8") as f:
            lines = f.readlines()

        python_obj = parser.toml_to_dict(lines)
        json_bytes = python_obj_to_pretty_json_bytes(python_obj)

        with open("output_dop1.json", "wb") as f:
            f.write(json_bytes)


    except FileNotFoundError:
        sys.stderr.write("Ошибка: Файл 'input.toml' не найден.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Ошибка при обработке: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
