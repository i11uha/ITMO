# Author = Safin Ilya Dmitrievich
# Group = P3106
# Date = 18.11.2025


class TOMLParser:
    def __init__(self):
        pass

    def _delete_comments(self, lines):
        result = []
        for line in lines:
            comment_index = line.find('#')
            if comment_index != -1:
                line = line[:comment_index]     # берём всё что находится до решётки
            result.append(line.strip())
        return result

    def _parse_string(self, s):

        s = s.strip()
        if s.startswith('"""'):  # многострочный примитив
            content = s[3:-3]
            content = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\"','"').replace('\\\\', '\\')
            content = content.replace('\\\n', '').replace('\\\r\n', '')  # обработка экранированных символов переноса
            return content
        elif s.startswith('"'):  # обычный примитив
            content = s[1:-1]
            content = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\"','"').replace('\\\\', '\\')
            return content
        elif s.startswith("'''"):
            return s[3:-3]
        elif s.startswith("'"):
            return s[1:-1]
        return s

    def _parse_scalar(self, s):     # определение типа данных
        s = s.strip()
        if not s:
            return None

        if s.lower() == "true":      # проверка на булево
            return True
        if s.lower() == "false":
            return False

        if s.startswith(('"', "'")):        # проверка на строку
            return self._parse_string(s)

        try:                       # проверка на целое число
            return int(s)
        except ValueError:
            pass

        try:                  # проверка рна дробное число
            return float(s)
        except ValueError:
            pass

        return s

    def _parse_array(self, s):      # парсинг списков
        s = s.strip()
        if not s.startswith('[') or not s.endswith(']'):
            raise ValueError(f"Неверный формат массива: {s}")

        content = s[1:-1].strip()
        if not content:
            return []

        elements = []
        i = 0
        start_idx = 0
        brace_level = 0 # brace_level - Уровень вложенности скобок
        quote_char = None # oтслеживание строк
        '''я не могу просто разделить строку по запятой, потому что
         запятые могут встречаться внутри вложенных массивов или внутри текстовых строк'''
        while i < len(content):
            char = content[i]
            if char == '[' or char == '{':
                brace_level += 1
            elif char == ']' or char == '}':
                brace_level -= 1
            elif char == '"' or char == "'":
                if quote_char is None:
                    quote_char = char
                elif quote_char == char:
                    quote_char = None

            if char == ',' and brace_level == 0 and quote_char is None:
                part = content[start_idx:i].strip()
                if part:
                    elements.append(self._parse_scalar(part))
                start_idx = i + 1
            i += 1
        last_part = content[start_idx:i].strip()
        if last_part:
            elements.append(self._parse_scalar(last_part))
        return elements

    def toml_to_dict(self, content_lines):
        if not content_lines:
            return {} # передали пустой список - получили пустой словарь
        content = self._delete_comments(content_lines)
        content = [line for line in content if line.strip()] # убрали пустые строки
        result = {} # "корневой" словарь
        current_table_ref = result # указатель словарей. изначально указывает на корень
        line_idx = 0
        while line_idx < len(content): # начинаем построчно перебирать
            line = content[line_idx]
            if line.startswith('[['):  # Таблица массивов
                table_path_str = line[2:-2].strip() # создаем список словарей по ключу
                keys = table_path_str.split('.')
                target_ref = result # текущий указатель. изначально корневой
                for i, key_part in enumerate(keys):
                    if i == len(keys) - 1:  # последний ключ - имя таблицы массива
                        if key_part not in target_ref:
                            target_ref[key_part] = [] # создаем ключ если его ещё не было
                        new_item = {}
                        target_ref[key_part].append(new_item) # добавляем словарь в список
                        current_table_ref = new_item
                    else:
                        if key_part in target_ref and isinstance(target_ref[key_part], list): # проверка на список
                            if not target_ref[key_part]:
                                target_ref[key_part].append({})
                            target_ref = target_ref[key_part][-1]
                        elif key_part not in target_ref:
                            target_ref[key_part] = {}
                            target_ref = target_ref[key_part] # если ключа нет - создаём
                        else:
                            target_ref = target_ref[key_part] # ечли есть - просто переходим
                line_idx += 1
                continue

            elif line.startswith('['): # создаем вложенный словарь
                table_path_str = line[1:-1].strip()
                keys = table_path_str.split('.')
                """Создаём цепочку вложенных словарей"""
                target_ref = result
                for key_part in keys:
                    if key_part not in target_ref:
                        target_ref[key_part] = {}
                    target_ref = target_ref[key_part]
                current_table_ref = target_ref
                line_idx += 1
                continue


            elif '=' in line:  # обработка ключей значений
                try:
                    key_part, value_part = line.split('=', 1)
                    key = key_part.strip()
                    dotted_keys = key.split('.')
                    temp_target = current_table_ref
                    for i, k in enumerate(dotted_keys): # k - текущая часть ключа, i - её индекс
                        if i == len(dotted_keys) - 1:
                            if value_part.strip().startswith('[') and value_part.strip().endswith(']'): # является ли значение массивом
                                temp_target[k] = self._parse_array(value_part)
                            else:
                                temp_target[k] = self._parse_scalar(value_part)
                        else:
                            if k not in temp_target:
                                temp_target[k] = {}
                            temp_target = temp_target[k]
                except ValueError: # на случай ошибок при split
                    pass
            line_idx += 1
        return result

    def parse(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f: # открытие файла в режиме чтения с кодировкой utf 8
            data_dict = self.toml_to_dict(f.readlines())
        return str(data_dict).encode('utf-8')


def toml_lines_to_bytes(lines):
    parser = TOMLParser()
    obj = parser.toml_to_dict(lines)
    return str(obj).encode('utf-8')


if __name__ == '__main__':
    parser = TOMLParser()

    try:
        binary_output = parser.parse("input.toml")
        import sys

        sys.stdout.buffer.write(binary_output)


    except FileNotFoundError:
        sys.stderr.write(
            "Файл 'input.toml' не найден.\n")
    except Exception as e:
        sys.stderr.write(f"Ошибка при парсинге: {e}\n")


