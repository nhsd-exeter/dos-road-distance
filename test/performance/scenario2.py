import json
from locust import HttpUser, task, LoadTestShape, tag, between
import config as config


class LoadFile:
    def __init__(self):
        self.file = "ccs_5_destinations.json"

    def set_file(self, file: str):
        self.file = file

    def get_file(self):
        return self.file


current_file = LoadFile()


class FiveDest(HttpUser):
    weight = 1
    wait_time = between(0.5, 2)
    host = config.BASE_HOST  # Add missing host configuration

    def on_start(self):
        # Load initial payload
        self.load_payload()

    def load_payload(self):
        """Load payload based on current file setting"""
        with open(f'{config.ccs_prefix}{current_file.get_file()}') as json_file:
            self.payload = json.load(json_file)

    @tag('load')
    @task
    def do_test(self):
        # Reload payload in case file has changed
        self.load_payload()
        self.client.post(config.API_ENDPOINT, data=json.dumps(self.payload), headers=config.headers)


class StepLoadShape(LoadTestShape):
    stages = [
        {"duration": 120, "users": 10, "spawn_rate": 5, "request_file": "ccs_50_destinations.json"},
        {"duration": 240, "users": 20, "spawn_rate": 10, "request_file": "ccs_50_destinations.json"},
        {"duration": 360, "users": 30, "spawn_rate": 15, "request_file": "ccs_50_destinations.json"},
        {"duration": 480, "users": 40, "spawn_rate": 20, "request_file": "ccs_50_destinations.json"},
        {"duration": 600, "users": 50, "spawn_rate": 25, "request_file": "ccs_50_destinations.json"},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                current_file.set_file(stage["request_file"])
                return tick_data
        return None
