import tomli
import json



def main():
    with open("input.toml", 'rb') as f:
        data = tomli.load(f)

    with open("output_dop2.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def toml_lines_to_json(toml_lines):
    toml_string = "".join(toml_lines)
    data = tomli.loads(toml_string)
    return json.dumps(data, ensure_ascii=False)

if __name__ == "__main__":
    main()