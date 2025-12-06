# Author = Safin Ilya Dmitrievich
# Group = P3106
# Date = 18.11.2025

from Main import TOMLParser
import sys


def _escape_xml_text(s):
    result = []
    for char in s:
        if char == '&':
            result.append('&amp;') # Амперсанд
        elif char == '<':
            result.append('&lt;')
        elif char == '>':
            result.append('&gt;')
        elif char == '"':
            result.append('&quot;')
        elif char == "'":
            result.append('&apos;')
        else:
            result.append(char)
    return ''.join(result)


def _dict_to_xml_worker(obj, tag_name, indent_level):
    indent_str = "  " * indent_level  # 2 пробела на уровень


    if obj is None:
        return f"{indent_str}<{tag_name}/>"

    elif isinstance(obj, bool): # обработка булевых
        text = "true" if obj else "false"
        return f"{indent_str}<{tag_name}>{_escape_xml_text(text)}</{tag_name}>"

    elif isinstance(obj, (int, float)): # числа целые и дробные
        text = str(obj)
        return f"{indent_str}<{tag_name}>{_escape_xml_text(text)}</{tag_name}>"

    elif isinstance(obj, str): # строки
        escaped = _escape_xml_text(obj)
        return f"{indent_str}<{tag_name}>{escaped}</{tag_name}>"

    elif isinstance(obj, list): # массивы
        if not obj:
            return f"{indent_str}<{tag_name}/>"
        lines = [f"{indent_str}<{tag_name}>"]
        for item in obj: # проходимся по массиву и реккурсивно используем _dict_to_xml_worker
            #каждый элемент списка сериализуем как <item>...</item>
            item_xml = _dict_to_xml_worker(item, "item", indent_level + 1)
            lines.append(item_xml)
        lines.append(f"{indent_str}</{tag_name}>")
        return '\n'.join(lines)

    elif isinstance(obj, dict): # словари
        if not obj:
            return f"{indent_str}<{tag_name}/>"
        lines = [f"{indent_str}<{tag_name}>"]
        for key, value in obj.items():
            if not isinstance(key, str):
                key = str(key)
            # имя тега = ключ словаря
            child_xml = _dict_to_xml_worker(value, key, indent_level + 1)
            lines.append(child_xml)
        lines.append(f"{indent_str}</{tag_name}>")
        return '\n'.join(lines)

    else:
        # fallback привести к строке
        text = _escape_xml_text(str(obj))
        return f"{indent_str}<{tag_name}>{text}</{tag_name}>"


def python_obj_to_xml(obj, root_tag: str = "root"):
    """преобразует обьект python в xml"""
    xml_content = _dict_to_xml_worker(obj, root_tag, 0)
    xml_str = f'<?xml version="1.0" encoding="utf-8"?>\n{xml_content}\n' # добавляем xml декларацию
    return xml_str.encode('utf-8') # кодируем в utf-8


def main():
    try:
        parser = TOMLParser()
        with open("input.toml", "r", encoding="utf-8") as f:
            lines = f.readlines()
        python_obj = parser.toml_to_dict(lines)

        xml_bytes = python_obj_to_xml(python_obj, "schedule_data")

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
    return python_obj_to_xml(obj, "schedule_data")

if __name__ == '__main__':
    main()
