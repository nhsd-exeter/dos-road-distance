import json
import config as config


class Common:
    # class Common:
    def fetch_file(self, file_path: str, file_name: str, bin: bool = False) -> dict:
        mode = "rb" if bin else "r"
        try:
            with open(file_path + file_name, mode=mode) as file_handle:
                file_content = file_handle.read()
                file_handle.close()

                return file_content
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
            raise ex

    def fetch_test_json(self, file_name: str) -> dict:
        json_file = self.fetch_file(config.PATH_TEST_JSON, file_name)
        return json.loads(json_file)

    def fetch_test_proto(self, file_name: str) -> dict:
        return self.fetch_file(config.PATH_TEST_PROTO, file_name)

    def fetch_test_proto_bin(self, file_name: str) -> dict:
        return self.fetch_file(config.PATH_TEST_PROTO, file_name, True)

    def fetch_mock_proto(self, file_name: str) -> dict:
        return self.fetch_file(config.PATH_MOCK_PROTO, file_name)

    def fetch_mock_proto_bin(self, file_name: str) -> dict:
        return self.fetch_file(config.PATH_MOCK_PROTO, file_name, True)
