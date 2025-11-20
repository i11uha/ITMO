
from Main import TOMLParser
import sys


def _escape_xml_text(s: str) -> str:
    result = []
    for char in s:
        if char == '&':
            result.append('&amp;')
        elif char == '<':
            result.append('<')
        elif char == '>':
            result.append('>')
        elif char == '"':
            result.append('&quot;')
        elif char == "'":
            result.append('&apos;')
        else:
            result.append(char)
    return ''.join(result)


def _dict_to_xml_worker(obj, tag_name: str, indent_level: int = 0) -> str:
    indent_str = "  " * indent_level  # 2 пробела на уровень
    inner_indent = "  " * (indent_level + 1)

    if obj is None:
        return f"{indent_str}<{tag_name}/>"

    elif isinstance(obj, bool):
        text = "true" if obj else "false"
        return f"{indent_str}<{tag_name}>{_escape_xml_text(text)}</{tag_name}>"

    elif isinstance(obj, (int, float)):
        if isinstance(obj, float):
            s = str(obj)
            if s in ('inf', '-inf', 'nan'):
                text = 'null'  # или raise — но для простоты null
            else:
                text = s
        else:
            text = str(obj)
        return f"{indent_str}<{tag_name}>{_escape_xml_text(text)}</{tag_name}>"

    elif isinstance(obj, str):
        escaped = _escape_xml_text(obj)
        return f"{indent_str}<{tag_name}>{escaped}</{tag_name}>"

    elif isinstance(obj, list):
        if not obj:
            return f"{indent_str}<{tag_name}/>"
        lines = [f"{indent_str}<{tag_name}>"]
        for item in obj:
            # Каждый элемент списка сериализуем как <item>...</item>
            item_xml = _dict_to_xml_worker(item, "item", indent_level + 1)
            lines.append(item_xml)
        lines.append(f"{indent_str}</{tag_name}>")
        return '\n'.join(lines)

    elif isinstance(obj, dict):
        if not obj:
            return f"{indent_str}<{tag_name}/>"
        lines = [f"{indent_str}<{tag_name}>"]
        for key, value in obj.items():
            if not isinstance(key, str):
                key = str(key)
            # Имя тега = ключ словаря
            child_xml = _dict_to_xml_worker(value, key, indent_level + 1)
            lines.append(child_xml)
        lines.append(f"{indent_str}</{tag_name}>")
        return '\n'.join(lines)

    else:
        # fallback: привести к строке
        text = _escape_xml_text(str(obj))
        return f"{indent_str}<{tag_name}>{text}</{tag_name}>"


def python_obj_to_pretty_xml_bytes(obj, root_tag: str = "root") -> bytes:
    xml_content = _dict_to_xml_worker(obj, root_tag, indent_level=0)
    xml_str = f'<?xml version="1.0" encoding="utf-8"?>\n{xml_content}\n'
    return xml_str.encode('utf-8')


def main():
    try:
        parser = TOMLParser()
        with open("input.toml", "r", encoding="utf-8") as f:
            lines = f.readlines()
        python_obj = parser.toml_to_dict(lines)

        xml_bytes = python_obj_to_pretty_xml_bytes(python_obj, root_tag="schedule_data")

        with open("output_dop3.xml", "wb") as f:
            f.write(xml_bytes)

    except FileNotFoundError:
        sys.stderr.write("Ошибка: Файл 'input.toml' не найден.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Ошибка при обработке: {e}\n")
        sys.exit(1)

def toml_lines_to_xml_bytes(lines):
    parser = TOMLParser()
    obj = parser.toml_to_dict(lines)
    return python_obj_to_pretty_xml_bytes(obj, root_tag="schedule_data")

if __name__ == '__main__':
    main()