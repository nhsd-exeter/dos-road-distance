import os

# Get API endpoint from environment variable (set by Kubernetes ConfigMap)
# or use a default for local development
API_ENDPOINT = os.getenv('API_ENDPOINT', 'http://localhost:8080')

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}

# Use absolute path that works in Docker container environment
# The mock files are copied to /opt/locust/mock/requests/ in the Docker build
if os.path.exists('/opt/locust/mock/requests/'):
    ccs_prefix = '/opt/locust/mock/requests/'
else:
    # Fallback for local development
    ccs_prefix = '../../application/roaddistance/mock/requests/'
