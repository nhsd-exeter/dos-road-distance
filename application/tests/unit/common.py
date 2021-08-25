import json


class Common:

    json_path: str = "tests/unit/test_json/"
    proto_path: str = "tests/unit/test_proto/"

    def fetch_json(self, file_name: str):
        try:
            with open(self.json_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))

    def fetch_proto(self, file_name: str):
        try:
            with open(self.proto_path + file_name) as proto_file:
                return proto_file.read()
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
