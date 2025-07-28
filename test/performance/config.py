import os

# Configuration for performance testing
# Set the base host URL - this should come from environment variables set by the deployment
# The environment variables PERF_TEST_HOST or LOCUST_HOST should be set by the Kubernetes deployment

# Enhanced debugging to understand what's happening
print("=== CONFIG.PY DEBUG START ===")
print(f"Environment PERF_TEST_HOST = '{os.environ.get('PERF_TEST_HOST', 'NOT SET')}'")
print(f"Environment LOCUST_HOST = '{os.environ.get('LOCUST_HOST', 'NOT SET')}'")
print(f"All environment variables containing 'HOST': {[(k, v) for k, v in os.environ.items() if 'HOST' in k.upper()]}")
print(f"All environment variables containing 'API': {[(k, v) for k, v in os.environ.items() if 'API' in k.upper()]}")

BASE_HOST = os.environ.get('PERF_TEST_HOST') or os.environ.get('LOCUST_HOST')

print(f"Resolved BASE_HOST = '{BASE_HOST}'")

# Validate that we have a valid base host configured
if not BASE_HOST or BASE_HOST.endswith('_TO_REPLACE'):
    print(f"ERROR: BASE_HOST validation failed. BASE_HOST='{BASE_HOST}'")
    raise ValueError("BASE_HOST not properly configured. PERF_TEST_HOST or LOCUST_HOST environment variable must be set to a valid API endpoint.")

API_ENDPOINT = '/'  # Your API Gateway route is POST /

print(f"Final configuration: BASE_HOST='{BASE_HOST}', API_ENDPOINT='{API_ENDPOINT}'")
print("=== CONFIG.PY DEBUG END ===")

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}
ccs_prefix = 'mock/requests/'
