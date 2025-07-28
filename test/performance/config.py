import os

# Get API endpoint from environment variable (set by Kubernetes ConfigMap)
# or use a default for local development
API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://api-nonprod.k8s-nonprod.texasplatform.uk/dosapi/roaddistance/v1/calculate')

headers = {'content-type': 'application/json', 'x-authorization': '', 'x-noauth': 'True'}
ccs_prefix = 'mock/requests/'
