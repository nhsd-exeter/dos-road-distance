import os

headers = {'content-type': 'application/json', 'x-authorization': os.environ['API_RD_TOKEN'], 'x-noauth': 'True'}
ccs_prefix = 'mock/requests/'
