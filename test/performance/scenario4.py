import json
import time
from locust import FastHttpUser, task, tag
import config as config


class TimeDelayStressUser(FastHttpUser):
    delay_increment = 30
    host = config.BASE_HOST

    def on_start(self):
        with open(config.ccs_prefix + 'ccs_500_destinations.json') as json_file:
            self.payload = json.dumps(json.load(json_file))  # Pre-serialize JSON
        self.delay_time = 0

    @tag('delay_stress')
    @task
    def delayed_request(self):
        with self.client.post(
            config.API_ENDPOINT,
            data=self.payload,
            headers=config.headers,
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")

        self.delay_time += self.delay_increment
        time.sleep(self.delay_time)  # Intentional delay for this test type