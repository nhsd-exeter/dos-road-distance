import json
import logging
from jsonschema import validate
from google.protobuf.json_format import Parse

class Provider():

    url = ''
    request = {}
    response = {}
    options = {}
    request_id = ''

    schema_path = '../../openapi_schemas/json/'

    contract_name = 'travel_time_api_json'

    def __init__(self, request):
        self.request = request
        #self.request_id = self.create_request_id()
        #self.logger = logging.getLogger(__name__, self.request_id)

        # this class also needs needs to
        # fetch the error code mapping for the given provider

        self.log(request)

    def log(self, request):
        pass

    def validate_against_schema(self, schema_name: str, json: dict) -> bool:
        try:
            schema = self.fetch_json(schema_name + '.json')
            return validate(schema=schema, instance=json) == None
        except Exception as ex:
            pass

    def fetch_json(self, file_name: str):
        try:
            with open(self.schema_path + file_name) as json_file:
                return json.load(json_file)
        except Exception as ex:
            print('Exception: Unable to open file ' + file_name + '. {0}'.format(ex))

