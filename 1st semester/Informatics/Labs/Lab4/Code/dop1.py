from Main import TOMLParser
import sys


def _escape_string(s: str) -> str:
    result = []
    for char in s:
        if char == '"':
            result.append('\\"')
        elif char == '\\':
            result.append('\\\\')
        elif char == '\n':
            result.append('\\n')
        elif char == '\r':
            result.append('\\r')
        elif char == '\t':
            result.append('\\t')
        elif char == '\b':
            result.append('\\b')
        elif char == '\f':
            result.append('\\f')
        else:
            result.append(char)
    return ''.join(result)


def _to_pretty_json_worker(obj, indent_level: int = 0) -> str:
    indent_str = "  " * indent_level  # 2 пробела на уровень

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
            items.append(_to_pretty_json_worker(item, indent_level + 1))
        inner = ',\n'.join('  ' + item for item in items)
        return '[\n' + inner + '\n' + indent_str + ']'
    elif isinstance(obj, dict):
        if not obj:
            return '{}'
        pairs = []
        for key, value in obj.items():
            if not isinstance(key, str):
                key = str(key)
            key_json = '"' + _escape_string(key) + '"'
            value_json = _to_pretty_json_worker(value, indent_level + 1)
            pairs.append('  ' + key_json + ': ' + value_json)
        inner = ',\n'.join(pairs)
        return '{\n' + inner + '\n' + indent_str + '}'
    else:
        return '"' + _escape_string(str(obj)) + '"'


def python_obj_to_pretty_json_bytes(obj) -> bytes:
    json_str = _to_pretty_json_worker(obj, indent_level=0)
    return (json_str + '\n').encode('utf-8')  # Добавляем \n в конец


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

def toml_lines_to_json_bytes(lines):
    parser = TOMLParser()
    obj = parser.toml_to_dict(lines)
    return python_obj_to_pretty_json_bytes(obj)


if __name__ == '__main__':
    main()