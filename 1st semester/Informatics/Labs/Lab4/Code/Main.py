# Author = Safin Ilya Dmitrievich
# Group = P3106
# Date = 18.11.2025

class TOMLParser:
    def __init__(self):
        pass

    def _find_pos(self, s: str, char: str) -> int:
        if s.count(char) == 0:
            return 10 ** 4
        else:
            return s.find(char)

    def _delete_comments(self, lines: list[str]) -> list[str]:
        result = []
        for line in lines:
            comment_index = line.find('#')
            if comment_index != -1:
                line = line[:comment_index]
            result.append(line.strip())
        return result

    def _parse_string(self, s: str) -> str:

        s = s.strip()
        if s.startswith('"""'):  # Multiline basic string
            content = s[3:-3]
            content = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\"',
                                                                                                     '"').replace(
                '\\\\', '\\')
            content = content.replace('\\\n', '').replace('\\\r\n', '')  # Handle escaped newlines
            return content
        elif s.startswith('"'):  # Basic string
            content = s[1:-1]
            content = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\"',
                                                                                                     '"').replace(
                '\\\\', '\\')
            return content
        elif s.startswith("'''"):
            return s[3:-3]
        elif s.startswith("'"):
            return s[1:-1]
        return s

    def _parse_scalar(self, s: str):
        s = s.strip()
        if not s:
            return None

        if s.lower() == "true":
            return True
        if s.lower() == "false":
            return False

        if s.startswith(('"', "'")):
            return self._parse_string(s)

        try:
            return int(s)
        except ValueError:
            pass

        try:
            return float(s)
        except ValueError:
            pass

        if ('T' in s or '-' in s) and ':' in s and len(s) >= 10:
            return s

        return s

    def _parse_array(self, s: str) -> list:
        s = s.strip()
        if not s.startswith('[') or not s.endswith(']'):
            raise ValueError(f"Invalid array format: {s}")

        content = s[1:-1].strip()
        if not content:
            return []

        elements = []
        i = 0
        start_idx = 0
        brace_level = 0
        quote_char = None

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

    def toml_to_dict(self, content_lines: list[str]) -> dict:
        if not content_lines:
            return {}

        content = self._delete_comments(content_lines)
        content = [line for line in content if line.strip()]

        result = {}
        current_table_ref = result

        line_idx = 0
        while line_idx < len(content):
            line = content[line_idx]

            if line.startswith('[['):  # Array Table
                table_path_str = line[2:-2].strip()
                keys = table_path_str.split('.')

                target_ref = result
                for i, key_part in enumerate(keys):
                    if i == len(keys) - 1:  # Last key is the name of the array table
                        if key_part not in target_ref:
                            target_ref[key_part] = []

                        new_item = {}
                        target_ref[key_part].append(new_item)
                        current_table_ref = new_item
                    else:
                        if key_part in target_ref and isinstance(target_ref[key_part], list):
                            if not target_ref[key_part]:
                                target_ref[key_part].append({})
                            target_ref = target_ref[key_part][-1]
                        elif key_part not in target_ref:
                            target_ref[key_part] = {}
                            target_ref = target_ref[key_part]
                        else:
                            target_ref = target_ref[key_part]
                line_idx += 1
                continue

            elif line.startswith('['):  # Standard Table
                table_path_str = line[1:-1].strip()
                keys = table_path_str.split('.')

                target_ref = result
                for key_part in keys:
                    if key_part not in target_ref:
                        target_ref[key_part] = {}
                    target_ref = target_ref[key_part]
                current_table_ref = target_ref
                line_idx += 1
                continue

            elif '=' in line:
                try:
                    key_part, value_part = line.split('=', 1)
                    key = key_part.strip()

                    dotted_keys = key.split('.')

                    temp_target = current_table_ref

                    for i, k in enumerate(dotted_keys):
                        if i == len(dotted_keys) - 1:
                            if value_part.strip().startswith(('"""', "'''")):
                                multiline_value_parts = [value_part.strip()]
                                start_quote = value_part.strip()[:3]

                                if not value_part.strip().endswith(start_quote):
                                    line_idx += 1
                                    while line_idx < len(content) and not content[line_idx].strip().endswith(
                                            start_quote):
                                        multiline_value_parts.append(content[line_idx])
                                        line_idx += 1
                                    if line_idx < len(content):
                                        multiline_value_parts.append(content[line_idx])

                                full_value_string = "\n".join(multiline_value_parts)
                                temp_target[k] = self._parse_scalar(full_value_string)
                            elif value_part.strip().startswith('[') and value_part.strip().endswith(']'):
                                temp_target[k] = self._parse_array(value_part)
                            else:
                                temp_target[k] = self._parse_scalar(value_part)
                        else:
                            if k not in temp_target:
                                temp_target[k] = {}
                            temp_target = temp_target[k]

                except ValueError:
                    pass
            line_idx += 1

        return result

    def parse_file_to_python_object_str_bytes(self, filepath: str) -> bytes:
        with open(filepath, 'r', encoding='utf-8') as f:
            data_dict = self.toml_to_dict(f.readlines())
        return str(data_dict).encode('utf-8')

    def parse_str_to_python_object_str_bytes(self, s: str) -> bytes:
        data_dict = self.toml_to_dict(s.split("\n"))
        return str(data_dict).encode('utf-8')

def toml_lines_to_bytes(lines):
    parser = TOMLParser()
    obj = parser.toml_to_dict(lines)
    return str(obj).encode('utf-8')


if __name__ == '__main__':
    parser = TOMLParser()

    try:
        binary_output = parser.parse_file_to_python_object_str_bytes("input.toml")
        import sys

        sys.stdout.buffer.write(binary_output)



    except FileNotFoundError:
        sys.stderr.write(
            "Ошибка: Файл 'input.toml' не найден. Пожалуйста, убедитесь, что файл существует и указан правильный путь.\n")
    except Exception as e:
        sys.stderr.write(f"Произошла ошибка при парсинге: {e}\n")


