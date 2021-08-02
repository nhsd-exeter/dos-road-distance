import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Convert:

    yaml_path: str = 'openapi_schemas/yaml/'
    contract_names: dict = {
        'provider': 'travel_time_api',
        'local': 'dos_road_distance_api'
    }
    contract_data: dict = {}


    def __init__(self):
        self.generate_contract_json()


    def generate_contract_json(self):
        try:
            for key in self.contract_names:
                file_name = self.yaml_path + self.contract_names[key] + '.yaml'
                with open(file_name) as yaml_file:
                    data = yaml.load(yaml_file.read(), Loader=Loader)
                    self.contract_data.update({key: self.fetch_content_from_schema(data)})
        except Exception as ex:
            raise Exception('file not found')
            print('Exception: Unable to open file ' + file_name + '. {0}'.format(ex))


    def fetch_content_from_schema(self, data: dict):
        for key, value in data.items():
            if key == 'schema':
                return value
            if isinstance(value, dict):
                rec = self.fetch_content_from_schema(value)
                if isinstance(rec, dict):
                    return rec
