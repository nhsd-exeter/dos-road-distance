import os
import json
import pytest
from road_distance_api.provider import Provider

class TestProvider():

    provider = provider()
    jsonPath:str = 'test_json/'

    def test_error_responses_handled_gracefully(self):
        for file in sorted(os.listdir(self.jsonPath)):
            if file.lower().find('_error_') != -1:
                json_content = self.fetch_json(file)
                http_status = json['http_status']

                try:
                    response = provider.format_response(json_content)
                    response_content = json.loads(response)

                    assert response_content['http_status'] == http_status
                    assert response_content['error_code'] is not None

                except ValueError as ve:
                    print('response returned by format_response is not valid json')
                    assert False
                except Exception as ex:
                    print('format_response has not handled an error state')
                    assert False

    def fetch_json(self, file_name: str):
        try:
            with open(self.jsonPath + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print('Exception: Unable to open file ' + file_name + '. {0}'.format(ex))
