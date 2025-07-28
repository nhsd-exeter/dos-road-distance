import json
import os
from locust import task, FastHttpUser, tag, between
import config as config

# Force the correct API Gateway URL regardless of environment
FORCED_API_HOST = "https://7bmdvfro69.execute-api.eu-west-2.amazonaws.com"
FORCED_API_ENDPOINT = "/"

# Debug: Print all relevant environment variables and configuration
print("=== DEBUG CONFIGURATION ===")
print(f"config.BASE_HOST = {config.BASE_HOST}")
print(f"config.API_ENDPOINT = {config.API_ENDPOINT}")
print(f"FORCED_API_HOST = {FORCED_API_HOST}")
print(f"FORCED_API_ENDPOINT = {FORCED_API_ENDPOINT}")
print(f"Environment PERF_TEST_HOST = {os.environ.get('PERF_TEST_HOST', 'NOT SET')}")
print(f"Environment LOCUST_HOST = {os.environ.get('LOCUST_HOST', 'NOT SET')}")
print("=== END DEBUG ===")


class FiveDest(FastHttpUser):
    weight = 80
    wait_time = between(0.5, 2)
    # Force the host to use our known working API Gateway URL
    host = FORCED_API_HOST

    def on_start(self):
        # Debug: Print host configuration when user starts
        print(f"DEBUG: User host = {self.host}")
        with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        print(f"DEBUG: Making request to {FORCED_API_ENDPOINT} with host {self.host}")
        response = self.client.post(FORCED_API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
        print(f"FiveDest response status: {response.status_code}")


class FiftyDest(FastHttpUser):
    weight = 15
    host = FORCED_API_HOST

    def on_start(self):
        # Debug: Print host configuration when user starts
        print(f"DEBUG: User host = {self.host}")
        with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        response = self.client.post(FORCED_API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
        print(f"FiftyDest response status: {response.status_code}")


class FiveHundredDest(FastHttpUser):
    weight = 3
    host = FORCED_API_HOST  # Set the host for this user class

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)


class OneThousandFiveHundredDest(FastHttpUser):
    weight = 1
    host = config.BASE_HOST  # Set the host for this user class

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)


class ThreeThousandDest(FastHttpUser):
    weight = 1
    host = config.BASE_HOST  # Set the host for this user class

    def on_start(self):
        with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
