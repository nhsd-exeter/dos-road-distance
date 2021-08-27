import json
import application.config as config


class Common:
    # class Common:
    def fetch_file(self, file_path: str, file_name: str) -> dict:
        try:
            with open(file_path + file_name) as file_handle:
                file_content = file_handle.read()
                file_handle.close()

                return file_content
        except Exception as ex:
            print("Exception: Unable to open file " + file_name + ". {0}".format(ex))
            raise ex

    def fetch_test_json(self, file_name: str):
        json_file = self.fetch_file(config.PATH_TEST_JSON, file_name)
        return json.loads(json_file)

    def fetch_test_proto(self, file_name: str):
        return self.fetch_file(config.PATH_TEST_PROTO, file_name)