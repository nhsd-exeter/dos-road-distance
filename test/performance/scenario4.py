import json
import time
from locust import FastHttpUser, task, tag, between
import config as config


class FiveHundredDest(FastHttpUser):
    delay_increment = 30
    host = config.BASE_HOST
    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.load(json_file)
        self.delay_time = 0

    @tag('load')
    @task
    def start_test(self):
        try:
            response = self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)
            response.raise_for_status()
        except Exception as e:
            print(f"Request failed: {e}")
        self.delay_time += self.delay_increment
        print(f"Sleeping for {self.delay_time} seconds after request.")
        time.sleep(self.delay_time)
