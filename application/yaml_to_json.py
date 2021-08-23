import os
import json

json_path: str = "openapi_schemas/json/"
yaml_path: str = "openapi_schemas/yaml/"
contract_infile: dict = {
    "local": "dos_road_distance_api",
    "provider": "travel_time_api",
    "provider_response": "travel_time_api",
}
contract_outfile: dict = {
    "local": "dos_road_distance_api",
    "provider": "travel_time_api",
    "provider_response": "travel_time_api_response",
}
schema_keys: dict = {"local": ["schema"], "provider": ["schema"], "provider_response": ["responses", 200, "schema"]}


def generate_contract_json():
    try:
        if not os.path.exists(json_path):
            os.makedirs(json_path)

        for key in contract_infile:
            print("Key: " + key)
            file_name = yaml_path + contract_infile[key] + ".yaml"
            print("Processing yaml for: " + file_name)

            with open(file_name) as yaml_file:
                data = yaml.load(yaml_file.read(), Loader=Loader)
                create_json(contract_outfile[key], parse_keys(schema_keys[key], data))
    except Exception as ex:
        print("Exception: Unable to open file " + file_name + ". {0}".format(ex))


def parse_keys(keys: list, data: dict):
    content = data
    for key in keys:
        content = fetch_content_from_schema(content, key)
    return content


def fetch_content_from_schema(data: dict, schema_key: str):
    for key, value in data.items():
        if key == schema_key:
            return value
        if isinstance(value, dict):
            rec = fetch_content_from_schema(value, schema_key)
            if isinstance(rec, dict):
                return rec


def create_json(file_name: str, contract_data: dict):
    with open(json_path + file_name + ".json", "w", encoding="utf-8") as f:
        json.dump(contract_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    generate_contract_json()
