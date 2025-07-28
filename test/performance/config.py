import os

# Get API endpoint from environment variable (set by Kubernetes ConfigMap)
# or use a default for local development
API_ENDPOINT = os.getenv('API_ENDPOINT', 'http://localhost:8080')

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}
ccs_prefix = '../../application/roaddistance/mock/requests/'
