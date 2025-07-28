import json
import os
from locust import task, FastHttpUser, tag, between
import config as config

# Use environment variable if set, otherwise use the known working API Gateway URL
API_HOST = os.environ.get('PERF_TEST_HOST', 'https://7bmdvfro69.execute-api.eu-west-2.amazonaws.com')
API_ENDPOINT = "/"

# Debug: Print all relevant environment variables and configuration
print("=== DEBUG CONFIGURATION ===")
print(f"config.BASE_HOST = {config.BASE_HOST}")
print(f"config.API_ENDPOINT = {config.API_ENDPOINT}")
print(f"API_HOST = {API_HOST}")
print(f"API_ENDPOINT = {API_ENDPOINT}")
print(f"Environment PERF_TEST_HOST = {os.environ.get('PERF_TEST_HOST', 'NOT SET')}")
print(f"Environment LOCUST_HOST = {os.environ.get('LOCUST_HOST', 'NOT SET')}")
print("=== END DEBUG ===")


class FiveDest(FastHttpUser):
    weight = 80
    wait_time = between(0.5, 2)
    # Use the configured host
    host = API_HOST

    def on_start(self):
        # Debug: Print host configuration when user starts
        print(f"DEBUG: User host = {self.host}")
        try:
            with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
                self.payload = json.load(json_file)
        except Exception as e:
            print(f"ERROR loading payload: {e}")
            # Fallback payload for testing
            self.payload = {
                "searchCriteria": {
                    "postcode": "LS1 4AP",
                    "searchDistance": 60
                },
                "destinations": [
                    {"postcode": "LS2 7UE", "name": "Location 1"},
                    {"postcode": "LS3 1LH", "name": "Location 2"},
                    {"postcode": "LS4 2HL", "name": "Location 3"},
                    {"postcode": "LS5 3RD", "name": "Location 4"},
                    {"postcode": "LS6 2QG", "name": "Location 5"}
                ]
            }

    @tag('load')
    @task
    def start_test(self):
        print(f"DEBUG: Making request to {API_ENDPOINT} with host {self.host}")
        try:
            response = self.client.post(API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
            print(f"FiveDest response status: {response.status_code}")
        except Exception as e:
            print(f"ERROR in request: {e}")


class FiftyDest(FastHttpUser):
    weight = 15
    host = API_HOST

    def on_start(self):
        # Debug: Print host configuration when user starts
        print(f"DEBUG: User host = {self.host}")
        try:
            with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
                self.payload = json.load(json_file)
        except Exception as e:
            print(f"ERROR loading payload: {e}")
            # Fallback payload for testing
            self.payload = {
                "searchCriteria": {
                    "postcode": "LS1 4AP",
                    "searchDistance": 60
                },
                "destinations": [
                    {"postcode": f"LS{i} 1AA", "name": f"Location {i}"} for i in range(1, 51)
                ]
            }

    @tag('load')
    @task
    def start_test(self):
        print(f"DEBUG: Making request to {API_ENDPOINT} with host {self.host}")
        try:
            response = self.client.post(API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
            print(f"FiftyDest response status: {response.status_code}")
        except Exception as e:
            print(f"ERROR in request: {e}")


class FiveHundredDest(FastHttpUser):
    weight = 3
    host = API_HOST

    def on_start(self):
        print(f"DEBUG: User host = {self.host}")
        try:
            with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
                self.payload = json.load(json_file)
        except Exception as e:
            print(f"ERROR loading payload: {e}")
            # Fallback payload for testing
            self.payload = {
                "searchCriteria": {
                    "postcode": "LS1 4AP",
                    "searchDistance": 60
                },
                "destinations": [
                    {"postcode": f"LS{i} 1AA", "name": f"Location {i}"} for i in range(1, 501)
                ]
            }

    @tag('load')
    @task
    def start_test(self):
        try:
            response = self.client.post(API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
            print(f"FiveHundredDest response status: {response.status_code}")
        except Exception as e:
            print(f"ERROR in request: {e}")


class OneThousandFiveHundredDest(FastHttpUser):
    weight = 1
    host = API_HOST

    def on_start(self):
        print(f"DEBUG: User host = {self.host}")
        try:
            with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
                self.payload = json.load(json_file)
        except Exception as e:
            print(f"ERROR loading payload: {e}")
            # Fallback payload for testing
            self.payload = {
                "searchCriteria": {
                    "postcode": "LS1 4AP",
                    "searchDistance": 60
                },
                "destinations": [
                    {"postcode": f"LS{i} 1AA", "name": f"Location {i}"} for i in range(1, 1501)
                ]
            }

    @tag('load')
    @task
    def start_test(self):
        try:
            response = self.client.post(API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
            print(f"OneThousandFiveHundredDest response status: {response.status_code}")
        except Exception as e:
            print(f"ERROR in request: {e}")


class ThreeThousandDest(FastHttpUser):
    weight = 1
    host = API_HOST

    def on_start(self):
        print(f"DEBUG: User host = {self.host}")
        try:
            with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
                self.payload = json.load(json_file)
        except Exception as e:
            print(f"ERROR loading payload: {e}")
            # Fallback payload for testing
            self.payload = {
                "searchCriteria": {
                    "postcode": "LS1 4AP",
                    "searchDistance": 60
                },
                "destinations": [
                    {"postcode": f"LS{i} 1AA", "name": f"Location {i}"} for i in range(1, 3001)
                ]
            }

    @tag('load')
    @task
    def start_test(self):
        try:
            response = self.client.post(API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
            print(f"ThreeThousandDest response status: {response.status_code}")
        except Exception as e:
            print(f"ERROR in request: {e}")
