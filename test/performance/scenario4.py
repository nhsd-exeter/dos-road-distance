import json
from locust import FastHttpUser, task, tag, between
import config as config


class FiveHundredDest(FastHttpUser):
    weight = 3
    wait_time = between(0.5, 2)  # Use proper wait_time instead of manual sleep
    host = config.BASE_HOST

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
        # Removed problematic manual delay logic that would cause exponential delays


class OneThousandFiveHundredDest(FastHttpUser):
    weight = 1
    wait_time = between(0.5, 2)
    host = config.BASE_HOST

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_1500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
        # Removed problematic manual delay logic that would cause exponential delays


class ThreeThousandDest(FastHttpUser):
    weight = 1
    wait_time = between(0.5, 2)
    host = config.BASE_HOST

    def on_start(self):
        with open(config.ccs_prefix + "ccs_3000_destinations.json") as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
        # Removed problematic manual delay logic that would cause exponential delays
