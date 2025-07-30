import os
import time

# Configuration for performance testing
# Set the base host URL - this should come from environment variables set by the deployment
# The environment variables PERF_TEST_HOST or LOCUST_HOST should be set by the Kubernetes deployment

def get_base_host_with_retry(max_retries=3, delay=1):
    """
    Get BASE_HOST with retry logic to handle timing issues where environment variables
    might not be immediately available when the container starts
    """
    for attempt in range(max_retries):
        perf_test_host = os.environ.get('PERF_TEST_HOST')
        locust_host = os.environ.get('LOCUST_HOST')

        print(f"=== CONFIG.PY DEBUG ATTEMPT {attempt + 1} ===")
        print(f"Environment PERF_TEST_HOST = '{perf_test_host}'")
        print(f"Environment LOCUST_HOST = '{locust_host}'")
        print(f"All environment variables containing 'HOST': {[(k, v) for k, v in os.environ.items() if 'HOST' in k.upper()]}")
        print(f"All environment variables containing 'API': {[(k, v) for k, v in os.environ.items() if 'API' in k.upper()]}")

        base_host = perf_test_host or locust_host

        if base_host and not base_host.endswith('_TO_REPLACE'):
            print(f"SUCCESS: Found valid BASE_HOST = '{base_host}' on attempt {attempt + 1}")
            return base_host

        if attempt < max_retries - 1:
            print(f"BASE_HOST not valid on attempt {attempt + 1}, retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            print(f"FAILED: No valid BASE_HOST found after {max_retries} attempts")

    return None

# Enhanced debugging to understand what's happening
print("=== CONFIG.PY DEBUG START ===")

BASE_HOST = get_base_host_with_retry()

print(f"Final resolved BASE_HOST = '{BASE_HOST}'")

# Validate that we have a valid base host configured
if not BASE_HOST or BASE_HOST.endswith('_TO_REPLACE'):
    print(f"ERROR: BASE_HOST validation failed. BASE_HOST='{BASE_HOST}'")
    print("Current environment variables:")
    for key, value in sorted(os.environ.items()):
        if any(keyword in key.upper() for keyword in ['HOST', 'API', 'LOCUST', 'PERF']):
            print(f"  {key} = '{value}'")
    raise ValueError("BASE_HOST not properly configured. PERF_TEST_HOST or LOCUST_HOST environment variable must be set to a valid API endpoint.")

API_ENDPOINT = '/'  # Your API Gateway route is POST /

print(f"Final configuration: BASE_HOST='{BASE_HOST}', API_ENDPOINT='{API_ENDPOINT}'")
print("=== CONFIG.PY DEBUG END ===")

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}
ccs_prefix = 'mock/requests/'
