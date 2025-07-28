import os

# Configuration for performance testing
# Set the base host URL - this should be your actual API Gateway URL
# Format: https://{api-id}.execute-api.{region}.amazonaws.com
BASE_HOST = os.environ.get('PERF_TEST_HOST', 'https://7bmdvfro69.execute-api.eu-west-2.amazonaws.com')
API_ENDPOINT = '/'  # Your API Gateway route is POST /

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}
ccs_prefix = 'mock/requests/'
