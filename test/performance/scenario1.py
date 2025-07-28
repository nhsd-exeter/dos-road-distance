import json
from locust import task, FastHttpUser, tag, between
import config as config

# Debug: Print configuration at module load time
print(f"DEBUG: BASE_HOST = {config.BASE_HOST}")
print(f"DEBUG: API_ENDPOINT = {config.API_ENDPOINT}")


class FiveDest(FastHttpUser):
    weight = 80
    wait_time = between(0.5, 2)
    host = config.BASE_HOST  # Set the host for this user class

    def on_start(self):
        # Debug: Print host configuration when user starts
        print(f"DEBUG: User host = {self.host}")
        with open(config.ccs_prefix + 'ccs_5_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        print(f"DEBUG: Making request to {config.API_ENDPOINT} with host {self.host}")
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)


class FiftyDest(FastHttpUser):
    weight = 15
    host = config.BASE_HOST  # Set the host for this user class

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_50_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)


class FiveHundredDest(FastHttpUser):
    weight = 3
    host = config.BASE_HOST  # Set the host for this user class

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
