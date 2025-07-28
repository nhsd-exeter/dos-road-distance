import json
import time
from locust import HttpUser, task, LoadTestShape, FastHttpUser, tag
import config as config


class FiveHundredDest(FastHttpUser):
    delay_increment = 30
    delay_time = 0
    host = config.API_ENDPOINT  # Set the host URL

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def start_test(self):
        self.client.post("", data=json.dumps(self.payload), headers=config.headers)
        self.delay_time += self.delay_increment
        time.sleep(self.delay_time)
