import os

# Configuration for performance testing
# Set the base host URL - this should come from environment variables set by the deployment
# The environment variables PERF_TEST_HOST or LOCUST_HOST should be set by the Kubernetes deployment
BASE_HOST = os.environ.get('PERF_TEST_HOST') or os.environ.get('LOCUST_HOST')

# Validate that we have a valid base host configured
if not BASE_HOST or BASE_HOST.endswith('_TO_REPLACE'):
    raise ValueError("BASE_HOST not properly configured. PERF_TEST_HOST or LOCUST_HOST environment variable must be set to a valid API endpoint.")

API_ENDPOINT = '/'  # Your API Gateway route is POST /

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}
ccs_prefix = 'mock/requests/'
